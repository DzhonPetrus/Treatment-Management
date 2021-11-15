const BASE_URL = `http://127.0.0.1:8000/`;

const getToken = () => (localStorage.getItem('session_token') === null) ? window.location.replace(`${BASE_URL}login`) : localStorage.getItem('session_token');
const getUserType = () => (localStorage.getItem('user_type') === null) ? window.location.replace(`${BASE_URL}login`) : localStorage.getItem('user_type');
const getUserId = () => (localStorage.getItem('user_id') === null) ? window.location.replace(`${BASE_URL}login`) : localStorage.getItem('user_id');
const getUserProfile = () => JSON.parse(localStorage.getItem('user_profile'));


const setToken = (token) => localStorage.setItem('session_token', token);
const removeToken = () => localStorage.removeItem('session_token');
const setUserType = (user_type) => localStorage.setItem('user_type', user_type);
const setUserId = (user_id) => localStorage.setItem('user_id', user_id);
const removeUserType = () => localStorage.removeItem('user_type');
const removeUserId = () => localStorage.removeItem('user_id');
const setUserProfile = (user_profile) => {
	localStorage.setItem('user_profile', user_profile);
	// window.user_profile = getUserProfile();
	// console.log(getUserProfile())
}
const removeUserProfile = () => localStorage.removeItem('user_profile');

if ((window.location.pathname !== '/login')){
	window.token = getToken();
	window.user_type = getUserType()
	window.user_profile = getUserProfile()
	window.user_id = getUserId()
	if((window.location.pathname.split('/')[1] !== `${window.user_type}`) && window.user_id)
		location.replace(`${BASE_URL}${window.user_type}/`);

}else {
	removeToken();
	removeUserType();
	removeUserProfile();
	removeUserId();
}
