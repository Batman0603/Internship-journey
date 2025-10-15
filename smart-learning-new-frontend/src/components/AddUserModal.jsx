import React, { useState } from 'react';
import { authAPI as api } from '../api/authAPI';
import Modal from '@mui/joy/Modal';
import ModalClose from '@mui/joy/ModalClose';
import ModalDialog from '@mui/joy/ModalDialog';
import DialogTitle from '@mui/joy/DialogTitle';
import DialogContent from '@mui/joy/DialogContent';
import Stack from '@mui/joy/Stack';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import Select from '@mui/joy/Select';
import Option from '@mui/joy/Option';
import Button from '@mui/joy/Button';
import FormHelperText from '@mui/joy/FormHelperText';

const AddUserModal = ({ isOpen, onClose, onUserAdded }) => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('student');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        try {
            const response = await api.post('/api/admin/users', {
                username,
                email,
                password,
                role,
            });
            setSuccess(response.message);
            // Pass the newly created user's ID back up
            if (onUserAdded) {
                onUserAdded({ id: response.user_id, username, email, role });
            }
            // Reset form and close modal after a short delay
            setTimeout(() => {
                onClose();
                setUsername('');
                setEmail('');
                setPassword('');
                setRole('student');
                setSuccess('');
            }, 1500);
        } catch (err) {
            setError(err.message || 'Failed to create user.');
        }
    };

    return (
        <Modal open={isOpen} onClose={onClose}>
            <ModalDialog>
                <ModalClose />
                <DialogTitle>Add New User</DialogTitle>
                <DialogContent>Fill in the information to create a new user.</DialogContent>
                <form onSubmit={handleSubmit}>
                    <Stack spacing={2}>
                        <FormControl required>
                            <FormLabel htmlFor="add-user-username">Username</FormLabel>
                            <Input id="add-user-username" name="username" autoFocus value={username} onChange={(e) => setUsername(e.target.value)} />
                        </FormControl>
                        <FormControl required>
                            <FormLabel htmlFor="add-user-email">Email</FormLabel>
                            <Input id="add-user-email" name="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
                        </FormControl>
                        <FormControl required>
                            <FormLabel htmlFor="add-user-password">Password</FormLabel>
                            <Input id="add-user-password" name="password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
                        </FormControl>
                        <FormControl>
                            <FormLabel>Role</FormLabel>
                            <Select value={role} onChange={(_, newValue) => setRole(newValue)}>
                                <Option value="student">Student</Option>
                                <Option value="teacher">Teacher</Option>
                                <Option value="admin">Admin</Option>
                            </Select>
                        </FormControl>
                        {error && <FormHelperText sx={{ color: 'danger.500' }}>{error}</FormHelperText>}
                        {success && <FormHelperText sx={{ color: 'success.500' }}>{success}</FormHelperText>}
                        <Button type="submit">Create User</Button>
                    </Stack>
                </form>
            </ModalDialog>
        </Modal>
    );
};

export default AddUserModal;