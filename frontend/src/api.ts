import axios from 'axios';

const api = axios.create({
    baseURL: 'http://172.31.45.56:8000',
    headers: {
        'Content-Type': 'application/json',
    },
});

export default api;
