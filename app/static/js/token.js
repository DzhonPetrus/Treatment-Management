const BASE_URL = `http://127.0.0.1:8000/`;

const getToken = () => (localStorage.getItem('session_token') === null) ? window.location.replace(`${BASE_URL}login`) : localStorage.getItem('session_token');
const getUserType = () => (localStorage.getItem('user_type') === null) ? window.location.replace(`${BASE_URL}login`) : localStorage.getItem('user_type');


const setToken = (token) => localStorage.setItem('session_token', token);
const removeToken = () => localStorage.removeItem('session_token');
const setUserType = (user_type) => localStorage.setItem('user_type', user_type);
const removeUserType = () => localStorage.removeItem('user_type');

if ((window.location.pathname !== '/login')){
	window.token = getToken();
	window.user_type = getUserType()
	if(window.location.pathname.split('/')[1] !== `${window.user_type}`)
		location.replace(`${BASE_URL}${window.user_type}/`);

}else {
	removeToken();
	removeUserType();

}