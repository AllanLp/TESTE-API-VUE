import os
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
import numpy as np
from flask_limiter import Limiter
from flask import Flask, request, jsonify
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_cors import CORS
import re
import html

# Configuração inicial
app = Flask(__name__)

# Configuração de segurança usando Talisman
Talisman(app, content_security_policy=None)  

# Configuração de CORS para limitar os domínios permitidos
CORS(app, resources={
    r"/operadoras/*": {
        "origins": [
            "http://localhost:8080",  # Acesso para sua aplicação Vue.js
            "http://127.0.0.1:5000"  # Acesso para testes via Postman
        ],
        "methods": ['POST'],  # Métodos permitidos
    }
})

# Configuração de rate limiting para evitar abuso
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"]  # Limita a 100 requisições por minuto
)

# Configuração da pasta de logs
log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Logs")
os.makedirs(log_directory, exist_ok=True)  # Cria a pasta Logs se não existir

# Configuração de Logs
log_file = os.path.join(log_directory, "api_logs.log")  # Caminho completo para o arquivo dentro da pasta Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API Logger")
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=3)  # Configura o arquivo de log
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Carregar dados do CSV
data = pd.read_csv('data/Relatorio_cadop.csv', delimiter=';')

# Função para validar os dados de entrada
def ValidarRequisicao(req_data):
    valid_columns = ['Registro_ANS', 'CNPJ', 'Razao_Social', 'Modalidade', 'Cidade', 'UF']
    valid_directions = ['Ascendente', 'Descendente']

    query = req_data.get('query', '')
    query = html.escape(query)  # Sanitiza a string da query
    order_by = req_data.get('order_by')
    order_dir = req_data.get('order_dir')

    # Validação de query
    if query and not isinstance(query, str):
        raise ValueError("A 'query' deve ser uma string.")

    # Validação de ordenação
    if order_by and order_by not in valid_columns:
        raise ValueError(f"Coluna de ordenação inválida. Colunas válidas: {', '.join(valid_columns)}")
    if order_dir and order_dir not in valid_directions:
        raise ValueError(f"Direção de ordenação inválida. Direções válidas: {', '.join(valid_directions)}")

@app.route('/operadoras', methods=['POST'])
@limiter.limit("50 per minute")  # Limita o número de requisições por IP
def BuscarOperadoras():
    try:
        logger.info(f"Requisição recebida de {request.remote_addr}")

        # Obtém os dados do corpo da requisição
        req_data = request.get_json()
        ValidarRequisicao(req_data)  

        query = req_data.get('query', '')
        order_by = req_data.get('order_by', 'Razao_Social')
        order_dir = req_data.get('order_dir', 'Ascendente')

        # Filtrar os resultados pela query
        resultados = data[data['Razao_Social'].str.contains(re.escape(query), case=False, na=False)]

        # Validar a coluna e aplicar ordenação diretamente
        if order_by in data.columns and order_dir in ['Ascendente', 'Descendente']:
            ascending = True if order_dir == 'Ascendente' else False
            resultados = resultados.sort_values(by=order_by, ascending=ascending)

        # Substituir NaN por valores padrão ("Não informado")
        resultados = resultados.replace({np.nan: "Não informado"})

        logger.info(f"Busca realizada. Total de registros encontrados: {len(resultados)}")
        return jsonify(resultados.to_dict(orient='records'))

    except ValueError as ve:
        logger.error(f"Erro de validação: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.critical(f"Erro inesperado: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    logger.info("Iniciando a API Flask...")
    app.run(debug=True)
