import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Altere depois para o domínio de produção
});

export default api;
