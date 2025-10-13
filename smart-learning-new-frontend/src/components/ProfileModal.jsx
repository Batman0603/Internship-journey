import React, { useState, useEffect } from 'react';
import { authAPI as api } from '../api/authAPI';
import Modal from '@mui/joy/Modal';
import ModalDialog from '@mui/joy/ModalDialog';
import Typography from '@mui/joy/Typography';
import Box from '@mui/joy/Box';

const ProfileModal = ({ isOpen, onClose }) => {
    const [userProfile, setUserProfile] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchProfile = async () => {
            if (isOpen && !userProfile) {
                try {
                    const profileData = await api.get('/user/profile');
                    setUserProfile(profileData);
                } catch (err) {
                    setError('Failed to fetch profile data.');
                }
            }
        };
        fetchProfile();
    }, [isOpen, userProfile]);

    return (
        <Modal open={isOpen} onClose={onClose}>
            <ModalDialog
                aria-labelledby="profile-modal-title"
                aria-describedby="profile-modal-description"
            >
                <Typography id="profile-modal-title" level="h4" component="h2">
                    User Profile
                </Typography>
                <Box id="profile-modal-description" sx={{ mt: 2 }}>
                    {error && <Typography color="danger">{error}</Typography>}
                    {userProfile ? (
                        <div>
                            <Typography><strong>Username:</strong> {userProfile.username}</Typography>
                            <Typography><strong>Email:</strong> {userProfile.email}</Typography>
                            <Typography><strong>Role:</strong> {userProfile.role}</Typography>
                        </div>
                    ) : (
                        !error && <Typography>Loading profile...</Typography>
                    )}
                </Box>
            </ModalDialog>
        </Modal>
    );
};

export default ProfileModal;