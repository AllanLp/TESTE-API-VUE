import axios from 'axios';

// Cria uma instância do axios com a configuração base
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000', // URL do backend
  headers: {
    'Content-Type': 'application/json',
  }
});

export default apiClient;