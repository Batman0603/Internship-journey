import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

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

        {/* Dashboard Routes */}
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/teacher/dashboard" element={<TeacherDashboard />} />
        <Route path="/student/dashboard" element={<StudentDashboard />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;