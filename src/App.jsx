import React, { useState } from "react";
import { BrowserRouter, useNavigate } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";

// Dummy session simulation (replace with token decode in production)
function getRoleFromToken(token) {
  try {
    return JSON.parse(atob(token.split('.')[1])).role;
  } catch {
    return null;
  }
}

export default function App() {
  const [token, setToken] = useState(null);
  const [role, setRole] = useState(null);

  const handleLogin = (token, role) => {
    setToken(token);
    setRole(role);
    // Optionally store in context or secure storage
  };

  return (
    <BrowserRouter>
      <AppRoutes isAuthenticated={!!token} role={role} onLogin={handleLogin} />
    </BrowserRouter>
  );
}
