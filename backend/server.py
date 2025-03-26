from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas


# Carregar dados do CSV
data = pd.read_csv('data/Relatorio_cadop.csv', delimiter=';')

@app.route('/operadoras', methods=['GET'])
def buscar_operadoras():
    query = request.args.get('query', '')
    resultados = data[data['Razao_Social'].str.contains(query, case=False, na=False)].head(10)

    # Substituir NaN por valores padrão (ex.: "Não informado")
    resultados = resultados.replace({np.nan: "Não informado"})

    return jsonify(resultados.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
