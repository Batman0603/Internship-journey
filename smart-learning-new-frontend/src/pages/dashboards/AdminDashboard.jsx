import React, { useState, useEffect } from 'react';
import { authAPI as api } from '../../api/authAPI';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';
import Avatar from '@mui/joy/Avatar';
import ProfileModal from '../../components/ProfileModal';

const AdminDashboard = () => {
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [isProfileOpen, setIsProfileOpen] = useState(false);


    useEffect(() => {
        const fetchDashboardData = async () => {
            try { // The backend endpoint for admin dashboard is /api/admin/dashboard
                const data = await api.get('/api/admin/dashboard');
                setMessage(data.message);
            } catch (err) {
                setError('Failed to fetch admin data. You might not have the correct permissions.');
                // Optional: Redirect if unauthorized
                if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                    navigate('/login');
                }
            }
        };

        fetchDashboardData();
    }, [navigate]);

    const handleLogout = async () => {
        try {
            await api.logout();
            navigate('/login');
        } catch (err) {
            setError('Logout failed. Please try again.');
        }
    };

    return (
        <>
            <nav className="dashboard-nav">
                <h2>Admin Dashboard</h2>
                <div className="dashboard-nav-actions" >
                    <Avatar variant="solid" className="profile-avatar" onClick={() => setIsProfileOpen(true)}>
                        P
                    </Avatar>
                    <button onClick={handleLogout} className="dashboard-logout-btn">Logout</button>
                </div>
            </nav>
            <div className="dashboard-container">
                {error ? (
                    <div className="dashboard-card">
                        <p className="error-message">{error}</p>
                    </div>
                ) : message ? (
                    <div className="dashboard-card">
                        <p className="dashboard-message">{message}</p>
                    </div>
                ) : <p>Loading...</p>}
            </div>
            <ProfileModal isOpen={isProfileOpen} onClose={() => setIsProfileOpen(false)} />
        </>
    );
};

export default AdminDashboard;