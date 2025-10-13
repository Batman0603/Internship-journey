import React, { useState, useEffect } from 'react';
import { authAPI as api } from '../../api/authAPI';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';
import Avatar from '@mui/joy/Avatar';
import ProfileModal from '../../components/ProfileModal';
// MUI Joy Imports for the table
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Table from '@mui/joy/Table';
import Sheet from '@mui/joy/Sheet';

const TeacherDashboard = () => {
    const [message, setMessage] = useState('');
    const [courses, setCourses] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [isProfileOpen, setIsProfileOpen] = useState(false);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const response = await api.get('/api/courses/all');
                setCourses(response.data || []);
                setMessage(`Welcome! Here are all courses on the platform.`);
            } catch (err) {
                setError('Failed to fetch teacher data. You might not have the correct permissions.');
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
                <h2>Teacher Dashboard</h2>
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
                ) : !message ? (
                    <p>Loading dashboard...</p>
                ) : (
                    <>
                        <div className="dashboard-card">
                            <p className="dashboard-message">{message}</p>
                        </div>
                        <Sheet
                            variant="outlined"
                            sx={{
                                width: '100%',
                                maxWidth: 1200,
                                borderRadius: 'sm',
                                boxShadow: 'sm',
                                mt: 4,
                            }}
                        >
                            <Table
                                borderAxis="bothBetween"
                                stripe="odd"
                                hoverRow
                                sx={{
                                    '& > thead > tr > th:first-child, & > tbody > tr > td:first-child': {
                                        position: 'sticky',
                                        left: 0,
                                        boxShadow: '1px 0 var(--TableCell-borderColor)',
                                        bgcolor: 'background.surface',
                                    },
                                }}
                            >
                                <thead>
                                    <tr>
                                        <th style={{ width: 250 }}>Course Title</th>
                                        <th style={{ width: 400 }}>Description</th>
                                        <th style={{ width: 160 }}>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {courses.map((course) => (
                                        <tr key={course.id}>
                                            <td>{course.title}</td>
                                            <td>{course.description}</td>
                                            <td>
                                                <Box sx={{ display: 'flex', gap: 1 }}>
                                                    <Button size="sm" variant="plain" color="neutral">View</Button>
                                                    <Button size="sm" variant="soft" color="primary">Manage</Button>
                                                </Box>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </Table>
                        </Sheet>
                    </>
                )}
            </div>
            <ProfileModal isOpen={isProfileOpen} onClose={() => setIsProfileOpen(false)} />
        </>
    );
};

export default TeacherDashboard;