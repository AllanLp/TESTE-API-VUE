import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import numpy as np
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect, generate_csrf
import re
import html

# Configuração inicial
app = Flask(__name__)

@app.route('/get_csrf_token', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    response = jsonify({"csrf_token": csrf_token})
    response.headers.set("X-CSRFToken", csrf_token)  # Alternativa: Configurar o cabeçalho
    return response

# Configuração de segurança usando Talisman
Talisman(app, content_security_policy=None)  # Desativa CSP para evitar bloqueio de cookies


# Configuração de chave secreta para CSRF
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "da64b159b57ea595749b4394c053e0d06731d8d92dbd72f62876a0231a460e5b01f5c425e803613019c228aa1b95439516d8587478c3f6ba92b88dc6564b9c19bb16cff9ac01cc5765029d0385b98f6e5c833dfe9fb0ede53c92448bd8967c84e5d22414a75aa387b4ce331c77d5a618133571137a5c0470d943402361573c49f5c9a1f00436249546459c532298595c65a59680163d31948bf189b3c966f476b2baaac0a685803eb294750d1d3e9e3f5c09548ff79d51308f7e6445f3501c0dcadebe1d662bdaff6c8a3d87d14138ee59d177465510e935659b8cf42144d962080070b890f964b387ded0dfec226529ff75d1f9282821d014a2bc43c87e8bc3")  # Usar variável de ambiente para maior segurança
csrf = CSRFProtect(app)
app.config['WTF_CSRF_CHECK_DEFAULT'] = False  # Opcional: desativa a verificação padrão para endpoints não CSRF


# Configuração de CORS para limitar os domínios permitidos
CORS(app, resources={
    r"/operadoras/*": {
        "origins": [
            "http://localhost:8080",  # Permitir acesso para sua aplicação Vue.js
            "http://127.0.0.1:5000"  # Permitir acesso para testes via Postman
        ],
        "methods": ['GET','POST'],  # Métodos permitidos
        "supports_credentials": True,  # Habilitar suporte a credenciais (cookies)
    },
    r"/get_csrf_token": {  # Permitir acesso ao endpoint para obter o token CSRF
        "origins": [
            "http://localhost:8080",  # Apenas o frontend Vue.js pode acessar
            "http://127.0.0.1:5000"
        ],
        "methods": ['GET'],  # Apenas método GET permitido
        "supports_credentials": True,  # Habilitar suporte a credenciais (cookies)
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
def validate_request_data(req_data):
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
def buscar_operadoras():
    try:
        logger.info(f"Requisição recebida de {request.remote_addr}")

        # Obtém os dados do corpo da requisição
        req_data = request.get_json()
        validate_request_data(req_data)  # Valida os dados da requisição

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
