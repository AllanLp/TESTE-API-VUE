import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';

const app = createApp(App);

// Configuração global do Axios
axios.defaults.baseURL = 'http://127.0.0.1:5000'; // URL do backend
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Adicione Axios ao app Vue
app.config.globalProperties.$http = axios;

app.config.devtools = true;


app.mount('#app');
