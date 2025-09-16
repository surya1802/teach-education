// frontend/config.js - DO NOT hardcode in other files, include this BEFORE app scripts
const API_BASE = (function() {
  // if running locally (dev)
  if (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost') {
    return 'http://127.0.0.1:8001/api';
  }
  // PRODUCTION: put your FastAPI service URL here (Render will show it after deploy)
  // Example: https://teach-api.onrender.com/api
  return 'https://REPLACE_WITH_YOUR_FASTAPI_SERVICE_URL/api';
})();
