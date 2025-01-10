import axios from "axios";

const api = axios.create({
  baseURL: "http://192.168.68.13:9998",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
