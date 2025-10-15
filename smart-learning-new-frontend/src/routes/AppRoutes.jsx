import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import ProtectedRoute from './ProtectedRoute';

// Auth Pages
import Login from '../pages/auth/Login';
import Signup from '../pages/auth/Signup';

// Dashboard Pages
import AdminDashboard from '../pages/dashboards/AdminDashboard';
import TeacherDashboard from '../pages/dashboards/TeacherDashboard';
import StudentDashboard from '../pages/dashboards/StudentDashboard';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        {/* Default route redirects to login */}
        <Route path="/" element={<Navigate to="/login" />} />

        {/* Auth Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Dashboard Routes (protected) */}
        <Route element={<ProtectedRoute allowedRoles={["admin"]} />}> 
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["teacher"]} />}> 
          <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={["student"]} />}> 
          <Route path="/student/dashboard" element={<StudentDashboard />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default AppRoutes;