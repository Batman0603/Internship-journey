import React from "react";
import { Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import Dashboard from "../pages/Dashboard";
import ProtectedRoute from "../layouts/ProtectedRoute";

export default function AppRoutes({ isAuthenticated, role, onLogin }) {
  return (
    <Routes>
      <Route path="/login" element={<Login onLogin={onLogin} />} />

      {/* Student Dashboard */}
      <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} role={role} requiredRole="student" />}>
        <Route path="/student/dashboard" element={<Dashboard role="student" />} />
      </Route>

      {/* Teacher Dashboard */}
      <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} role={role} requiredRole="teacher" />}>
        <Route path="/teacher/dashboard" element={<Dashboard role="teacher" />} />
      </Route>

      {/* Admin Dashboard */}
      <Route element={<ProtectedRoute isAuthenticated={isAuthenticated} role={role} requiredRole="admin" />}>
        <Route path="/admin/dashboard" element={<Dashboard role="admin" />} />
      </Route>

      {/* Default route */}
      <Route path="*" element={<Login onLogin={onLogin} />} />
    </Routes>
  );
}
