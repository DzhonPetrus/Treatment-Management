const BASE_URL = `http://127.0.0.1:8000/`;

const getToken = () => (localStorage.getItem('session_token') === null) ? window.location.replace(`${BASE_URL}login`) : localStorage.getItem('session_token');


const setToken = (token) => localStorage.setItem('session_token', token);
const removeToken = () => localStorage.removeItem('session_token');

if (!(window.location.pathname == '/login'))
	window.token = getToken();