import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import toast from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';

const app = createApp(App);

// Configuração global do Axios
axios.defaults.baseURL = 'http://127.0.0.1:5000'; // URL do backend
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Adicione Axios ao app Vue
app.config.globalProperties.$http = axios;

app.config.devtools = true;

// Use o Vue3-Toastify
app.use(toast);

app.mount('#app');
