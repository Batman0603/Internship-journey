import React, { useState, useEffect } from 'react';
import { authAPI as api } from "../../api/authAPI";
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

import Avatar from '@mui/joy/Avatar';
import Box from '@mui/joy/Box';
import Button from '@mui/joy/Button';
import Table from '@mui/joy/Table';
import Sheet from '@mui/joy/Sheet';
import Chip from '@mui/joy/Chip';
import Input from '@mui/joy/Input';
import IconButton from '@mui/joy/IconButton';
import Typography from '@mui/joy/Typography';
import { Search, KeyboardArrowRight, KeyboardArrowLeft } from '@mui/icons-material';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import ProfileModal from '../../components/ProfileModal';

const StudentDashboard = () => {
    const [message, setMessage] = useState('');
    const [courses, setCourses] = useState([]);
    const [error, setError] = useState('');
    const [isProfileOpen, setIsProfileOpen] = useState(false);
    const navigate = useNavigate();

    // State for pagination, filtering, and sorting
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [filter, setFilter] = useState('');
    const [sort, setSort] = useState('title_asc');
    const [limit] = useState(10); // Items per page

    useEffect(() => {
        const fetchDashboardData = async () => {
            try {
                // Construct the API endpoint with query parameters
                const params = new URLSearchParams({
                    page,
                    limit,
                    sort,
                });
                if (filter) {
                    params.append('category', filter);
                }

                const response = await api.get(`/api/courses?${params.toString()}`);
                
                setCourses(response.data || []);
                setTotalPages(response.total_pages || 1);
                setMessage(`Welcome! Here are the available courses.`);
            } catch (err) {
                setError(err.message || 'Failed to fetch student data. You might not have the correct permissions.');
                if (err.response && (err.response.status === 401 || err.response.status === 403)) {
                    navigate('/login');
                }
            }
        };

        fetchDashboardData();
    }, [navigate, page, filter, sort, limit]);

    const handleLogout = async () => {
        try {
            await api.logout();
            navigate('/login');
        } catch (err) {
            setError('Logout failed. Please try again.');
        }
    };

    const handleEnroll = async (courseId) => {
        try {
            await api.post(`/api/courses/${courseId}/enroll`);
            // Refresh the dashboard data to show the new enrollment status
            setCourses(courses.map(course => 
                course.id === courseId ? { ...course, is_enrolled: true } : course
            ));
        } catch (err) {
            setError(`Failed to enroll in course ${courseId}. Please try again.`);
        }
    };

    const handleViewCourse = (courseId) => {
        // Future implementation: navigate to a detailed course view page
        console.log(`Navigate to course view for ${courseId}`);
    };

    return (
        <>
            <nav className="dashboard-nav">
                <h2>Student Dashboard</h2>
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

                        {/* Filter and Sort Controls */}
                        <Box
                            className="table-controls"
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between',
                                mt: 2,
                                mb: 1,
                                width: '100%',
                                maxWidth: 1200,
                            }}
                        >
                            <Input
                                startDecorator={<Search />}
                                placeholder="Filter by course title..."
                                value={filter}
                                onChange={(e) => {
                                    setFilter(e.target.value);
                                    setPage(1); // Reset to first page on new filter
                                }}
                                sx={{ flexGrow: 1, mr: 2 }}
                            />
                            <Select
                                value={sort}
                                onChange={(e, newValue) => {
                                    setSort(newValue);
                                    setPage(1); // Reset to first page on new sort
                                }}
                                sx={{ minWidth: 200 }}
                            >
                                <Option value="title_asc">Title (A-Z)</Option>
                                <Option value="title_desc">Title (Z-A)</Option>
                                <Option value="newest">Newest</Option>
                                <Option value="oldest">Oldest</Option>
                            </Select>
                        </Box>


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
                                                {course.is_enrolled ? (
                                                    <Chip color="success" variant="soft">Enrolled</Chip>
                                                ) : (
                                                    <Chip color="neutral" variant="outlined">Not Enrolled</Chip>
                                                )}
                                            </td>
                                            <td>
                                                {course.is_enrolled ? (
                                                    <Button size="sm" variant="outlined" onClick={() => handleViewCourse(course.id)}>View Course</Button>
                                                ) : (
                                                    <Button size="sm" variant="solid" color="primary" onClick={() => handleEnroll(course.id)}>Enroll</Button>
                                                )}
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
            <ProfileModal isOpen={isProfileOpen} onClose={() => setIsProfileOpen(false)} />
        </>
    );
};

export default StudentDashboard;
