const API_URL = "https://wlcritters.herokuapp.com/";
const OAUTH_URL = "wlcritters.us.auth0.com";
const API_ID = "https://wlcritters.com/volunteerHub";
const CLIENT_ID = "3rV6cklWQDFjbByAI0V2aHG5NCwsI7rn";
const CALLBACK_URL = "https://wlcritters.000webhostapp.com/login.html";

const LOGIN_URL = "https://" + OAUTH_URL + "/authorize?audience=" + API_ID + "&response_type=token&client_id=" + CLIENT_ID +
    "&redirect_uri=" + CALLBACK_URL;
const LOGOUT_URL =  API_URL + "vHub/logout";
const PERMISSIONS_API = "vHub/apps";