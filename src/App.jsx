import React, { useState } from "react";
import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";

export default function App() {
  const [token, setToken] = useState(null);
  const [role, setRole] = useState(null);

  const handleLogin = (token, role) => {
    setToken(token);
    setRole(role);
  };

  return (
    <BrowserRouter>
      <AppRoutes isAuthenticated={!!token} role={role} onLogin={handleLogin} />
    </BrowserRouter>
  );
}
