import axios from "axios";

export function login(role, credentials) {
  return axios.post(`/api/auth/login?role=${role}`, credentials, {
    withCredentials: true // send cookies
  });
}

export function refreshToken() {
  return axios.post("/api/auth/refresh", {}, { withCredentials: true });
}

export function logout() {
  return axios.post("/api/auth/logout", {}, { withCredentials: true });
}
