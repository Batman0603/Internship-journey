import React, { useState, useEffect } from 'react';
import { authAPI as api } from '../../api/authAPI';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';
import Avatar from '@mui/joy/Avatar';
import AddUserModal from '../../components/AddUserModal';
import ProfileModal from '../../components/ProfileModal';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Table from '@mui/joy/Table';
import Sheet from '@mui/joy/Sheet';
import Chip from '@mui/joy/Chip';
import IconButton from '@mui/joy/IconButton';
import Typography from '@mui/joy/Typography';
import AddIcon from '@mui/icons-material/Add';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';

const AdminDashboard = () => {
    const [message, setMessage] = useState('');
    const [users, setUsers] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const [isProfileOpen, setIsProfileOpen] = useState(false);
    const [isAddUserModalOpen, setAddUserModalOpen] = useState(false);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [limit] = useState(10);

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                // Fetch summary message (if any) and list of users for admin table
                const params = new URLSearchParams({ page, limit });

                // The backend endpoint for admin dashboard is /admin/dashboard
                // The backend endpoint for users is /admin/users
                const [dashboardRes, usersRes] = await Promise.all([
                    api.get('/api/admin/dashboard'),
                    api.get(`/api/admin/users?${params.toString()}`),
                ]);

                setMessage(dashboardRes.message);
                setUsers(usersRes.data || []);
                setTotalPages(usersRes.totalPages || 1);
            } catch (errMain) {
                setError('Failed to fetch admin data. You might not have the correct permissions.');
                // Optional: Redirect if unauthorized
                if (errMain?.response && (errMain.response.status === 401 || errMain.response.status === 403)) {
                    navigate('/login');
                }
            }
        };

        fetchDashboardData();
    }, [navigate, page, limit]);

    const handleLogout = async () => {
        try {
            await api.logout();
            navigate('/login');
        } catch {
            setError('Logout failed. Please try again.');
        }
    };

    const handleUserAdded = () => {
        // A new user has been added, refetch the first page to see the new user.
        setPage(1);
    };

    return (
        <>
            <nav className="dashboard-nav">
                <h2>Admin Dashboard</h2>
                <div className="dashboard-nav-actions" >
                    <Button
                        startDecorator={<AddIcon />}
                        onClick={() => setAddUserModalOpen(true)}
                    >
                        Add User
                    </Button>
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
                                        <th style={{ width: 'var(--Table-firstColumnWidth)' }}>Name</th>
                                        <th style={{ width: '40%' }}>Email</th>
                                        <th style={{ width: '15%' }}>Role</th>
                                        <th style={{ width: '20%' }}>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {users.map((user) => (
                                        <tr key={user.id}>
                                            <td>{user.username || user.name || user.email}</td>
                                            <td>{user.email}</td>
                                            <td>
                                                <Chip color={user.role === 'admin' ? 'danger' : 'neutral'} variant="soft">{user.role || 'user'}</Chip>
                                            </td>
                                            <td>
                                                <Box sx={{ display: 'flex', gap: 1 }}>
                                                    <Button size="sm" variant="outlined">View</Button>
                                                    <Button size="sm" variant="soft" color="primary">Make Admin</Button>
                                                    <Button size="sm" variant="plain" color="danger">Remove</Button>
                                                </Box>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </Table>
                        </Sheet>

                        {/* Pagination Controls */}
                        <Box
                            className="table-pagination"
                            sx={{
                                display: 'flex',
                                justifyContent: 'flex-end',
                                alignItems: 'center',
                                gap: 2,
                                mt: 2,
                                width: '100%',
                                maxWidth: 1200,
                            }}
                        >
                            <IconButton
                                size="sm"
                                color="neutral"
                                variant="outlined"
                                disabled={page <= 1}
                                onClick={() => setPage(page - 1)}
                            >
                                <KeyboardArrowLeft />
                            </IconButton>
                            <Typography>Page {page} of {totalPages}</Typography>
                            <IconButton
                                size="sm"
                                color="neutral"
                                variant="outlined"
                                disabled={page >= totalPages}
                                onClick={() => setPage(page + 1)}
                            >
                                <KeyboardArrowRight />
                            </IconButton>
                        </Box>
                    </>
                )}
            </div>
            <AddUserModal
                isOpen={isAddUserModalOpen}
                onClose={() => setAddUserModalOpen(false)}
                onUserAdded={handleUserAdded}
            />
            <ProfileModal isOpen={isProfileOpen} onClose={() => setIsProfileOpen(false)} />
        </>
    );
};

export default AdminDashboard;