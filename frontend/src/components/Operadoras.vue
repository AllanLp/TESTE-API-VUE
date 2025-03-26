<template>
    <div>
        <h1>Buscar Operadoras</h1>

        <div class="container">
            <div class="search">
                <input type="text" v-model="query" placeholder="Razao Social da Operadora" />
                <button @click="buscarOperadoras">Buscar</button>
            </div>

            <div class="cards">
                <div class="card" v-for="operadora in operadoras" :key="operadora.Registro_ANS">
                    <div class="card-content">
                        <h2><i class="fas fa-building"></i> {{ operadora.Razao_Social || "Não informado" }}</h2>
                        <ul>
                            <li>
                                <strong><i class="fas fa-map-marker-alt"></i> Cidade:</strong> {{ operadora.Cidade ||
                                "Não especificada" }}
                            </li>
                            <li>
                                <strong><i class="fas fa-location-arrow"></i> UF:</strong> {{ operadora.UF || "Não informado" }}
                            </li>
                            <li>
                                <strong><i class="fas fa-id-card"></i> Registro ANS:</strong> {{ operadora.Registro_ANS
                                || "Não informado" }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>
  
  <script>
  import apiClient from "../services/api";
  
  export default {
    name: "ListaOperadoras", 
    data() {
        return {
            operadoras: [],
            query: ""
            
        };
    },
    methods: {
      buscarOperadoras() {
        apiClient.get(`/operadoras?query=${this.query}`)
          .then(response => {
            
            this.operadoras = response.data;

          })
          .catch(error => {
            console.error("Erro ao buscar operadoras:", error);
          });
      }
    }
  };
  </script>
  
  <style>
.container {
  margin: 20px;
}

.search {
  margin-bottom: 40px; /* Espaçamento entre input e os cartões */
  display: flex;
  justify-content: center;
  gap: 10px;
}

input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  width: 300px;
}

button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-evenly;
}

.card {
  border: 1px solid #ddd;
  padding: 16px;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 300px;
}

.card-content h2 {
  font-size: 1.2em;
  margin-bottom: 12px;
}

.card-content ul {
  list-style: none;
  padding: 0;
}

.card-content ul li {
  margin: 8px 0;
}

.card-content ul li strong {
  margin-right: 5px;
}

.card-content ul li i {
  margin-right: 8px;
}
</style>
  
  
