import React from "react";
import { Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import ProtectedRoute from "../layouts/ProtectedRoute";

export default function AppRoutes({ isAuthenticated, role, onLogin }) {
  return (
    <Routes>
      <Route path="/login" element={<Login onLogin={onLogin} />} />
      <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} role={role} requiredRole="student" />}>
        <Route path="/student/dashboard" element={<Dashboard role="student" />} />
      </Route>
      <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} role={role} requiredRole="teacher" />}>
        <Route path="/teacher/dashboard" element={<Dashboard role="teacher" />} />
      </Route>
      <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} role={role} requiredRole="admin" />}>
        <Route path="/admin/dashboard" element={<Dashboard role="admin" />} />
      </Route>
      <Route path="*" element={<Login onLogin={onLogin} />} />
    </Routes>
  );
}
