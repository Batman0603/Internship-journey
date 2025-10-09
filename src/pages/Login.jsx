import React from "react";
import LoginForm from "../components/LoginForm";

export default function Login({ onLogin }) {
  return (
    <div>
      <h2 className="text-2xl mt-8 text-center">Role-Based Login</h2>
      <LoginForm onLogin={onLogin} />
    </div>
  );
}
