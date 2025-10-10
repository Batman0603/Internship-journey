import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from '../pages/auth/Login.jsx';
import Signup from '../pages/auth/Signup.jsx';

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </BrowserRouter>
  );
}
