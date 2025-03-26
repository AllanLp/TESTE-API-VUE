from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  

# Carregar dados do CSV
data = pd.read_csv('data/Relatorio_cadop.csv', delimiter=';')

@app.route('/operadoras', methods=['GET'])
def buscar_operadoras():
    try:
        # Obtém os parâmetros da requisição
        query = request.args.get('query', '') 
        order_by = request.args.get('order_by', 'Razao_Social')  # Coluna para ordenação
        order_dir = request.args.get('order_dir', 'Ascendente')  # Direção da ordenação: Ascendente ou Descendente

        # Filtrar os resultados pela query
        resultados = data[data['Razao_Social'].str.contains(query, case=False, na=False)]

        # Validar a coluna e aplicar ordenação diretamente
        if order_by in data.columns and order_dir in ['Ascendente', 'Descendente']:
            ascending = True if order_dir == 'Ascendente' else False
            resultados = resultados.sort_values(by=order_by, ascending=ascending)

        # Substituir NaN por valores padrão ("Não informado")
        resultados = resultados.replace({np.nan: "Não informado"})

        # Retornar os resultados como JSON
        return jsonify(resultados.to_dict(orient='records'))
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
