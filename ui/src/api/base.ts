import axios from "axios";

const api = axios.create({
  baseURL: "http://flask_app:8080",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
