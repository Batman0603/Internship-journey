import React, { useState } from "react";
import { login } from "../api/auth";

export default function LoginForm({ onLogin }) {
  const [role, setRole] = useState("student");
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [error, setError] = useState(null);

  const handleChange = e => setCredentials({ ...credentials, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const { data } = await login(role, credentials);
      setError(null);
      onLogin(data.token, data.role);
    } catch (err) {
      setError("Invalid login");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 max-w-xs mx-auto mt-10">
      <select value={role} onChange={e => setRole(e.target.value)} className="border p-2">
        <option value="student">Student</option>
        <option value="teacher">Teacher</option>
        <option value="admin">Admin</option>
      </select>
      <input name="username" placeholder="Username" value={credentials.username} onChange={handleChange} className="border p-2" />
      <input name="password" type="password" placeholder="Password" value={credentials.password} onChange={handleChange} className="border p-2" />
      <button type="submit" className="bg-blue-600 text-white p-2">Login</button>
      {error && <div className="text-red-600">{error}</div>}
    </form>
  );
}
