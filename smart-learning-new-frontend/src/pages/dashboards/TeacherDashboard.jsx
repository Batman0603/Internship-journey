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

import Chip from '@mui/joy/Chip'; // <-- Add this line
// ... other imports

const TeacherDashboard = () => {
    const [message, setMessage] = useState('');
    const [courses, setCourses] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [isProfileOpen, setIsProfileOpen] = useState(false);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                const response = await api.get('/api/courses');
                setCourses(response.data || []);
                setMessage(`Welcome! Here are all courses on the platform.`);
            } catch (err) {
                setError('Failed to fetch teacher data. You might not have the correct permissions.');
                if (err?.response && (err.response.status === 401 || err.response.status === 403)) {
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
        } catch {
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
                                '--TableCell-height': '40px',
                                '--TableHeader-height': 'calc(1 * var(--TableCell-height))',
                                '--Table-firstColumnWidth': '250px',
                                '--Table-lastColumnWidth': '160px',
                                '--TableRow-stripeBackground': 'rgba(0 0 0 / 0.04)',
                                '--TableRow-hoverBackground': 'rgba(0 0 0 / 0.08)',
                                overflow: 'auto',
                                backgroundColor: 'background.surface',
                            }}
                        >
                            <Table
                                borderAxis="bothBetween"
                                stripe="odd"
                                hoverRow
                                sx={{
                                    '& > thead > tr > th:first-of-type, & > tbody > tr > td:first-of-type': {
                                        position: 'sticky',
                                        left: 0,
                                        boxShadow: '1px 0 var(--TableCell-borderColor)',
                                        bgcolor: 'background.surface',
                                    },
                                    '& > thead > tr > th:last-child, & > tbody > tr > td:last-child': {
                                        position: 'sticky',
                                        right: 0,
                                        bgcolor: 'var(--TableCell-headBackground)',
                                    },
                                }}
                            >
                                <thead>
                                    <tr>
                                        <th style={{ width: 'var(--Table-firstColumnWidth)' }}>Course Title</th>
                                        <th style={{ width: '40%' }}>Description</th>
                                        <th style={{ width: '15%' }}>Status</th>
                                        <th style={{ width: '20%' }}>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {courses.map((course) => (
                                        <tr key={course.id}>
                                            <td>{course.title}</td>
                                            <td>{course.description}</td>
                                            <td>
                                                <Chip color="primary" variant="soft">Published</Chip>
                                            </td>
                                            <td>
                                                <Box sx={{ display: 'flex', gap: 1 }}>
                                                    <Button size="sm" variant="outlined" onClick={() => console.log('View', course.id)}>View</Button>
                                                    <Button size="sm" variant="soft" color="primary" onClick={() => console.log('Manage', course.id)}>Manage</Button>
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