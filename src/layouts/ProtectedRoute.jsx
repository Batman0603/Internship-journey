import React from "react";
import { Navigate, Outlet } from "react-router-dom";

export default function ProtectedRoute({ isAuthenticated, role, requiredRole }) {
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  if (role !== requiredRole) return <Navigate to={`/${role}/dashboard`} replace />;
  return <Outlet />;
}
