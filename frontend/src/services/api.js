import axios from 'axios';

// Cria uma instância do axios com a configuração base
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000', // URL do backend
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Garante que cookies sejam enviados e recebidos
});

// Adiciona um interceptor para incluir o token CSRF automaticamente
apiClient.interceptors.request.use(async (config) => {
  if (config.method === 'post') {
    try {
      // Obtém o token CSRF do endpoint
      const csrfResponse = await axios.get('http://127.0.0.1:5000/get_csrf_token', { withCredentials: true });
      const csrfToken = csrfResponse.data.csrf_token;

      // Adiciona o token CSRF no cabeçalho
      config.headers['X-CSRFToken'] = csrfToken;
    } catch (error) {
      console.error('Erro ao obter o token CSRF:', error);
    }
  }
  return config;
});

export default apiClient;
