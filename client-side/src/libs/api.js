// axios
import axios from "axios";

export const subdomains = {
  node: process.env.VUE_APP_NODE_ENV || "http://127.0.0.1:3000",
  movies: process.env.VUE_APP_MOVIES_ENV || "http://127.0.0.1:8000",
};


export const axiosIns = {};
// eslint-disable-next-line no-restricted-syntax
Object.keys(subdomains).forEach((subdomain) => {
  axiosIns[subdomain] = axios.create({
    baseURL: subdomains[subdomain] + "/api",
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods":
        "GET, POST, PATCH, PUT, DELETE, OPTIONS, HEAD",
      "Access-Control-Allow-Headers": "Origin, Content-Type, X-Auth-Token",
    },
  });
});

const api = (sub) => axiosIns[sub];

export default api;
