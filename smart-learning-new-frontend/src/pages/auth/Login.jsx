import React, { useState } from 'react';
import './login.css';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../../api/authAPI.js';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        try {
            // The login API returns the user's role, which we'll use for redirection.
            const response = await authAPI.login(email, password);
            const { role } = response;

            // Redirect to the correct dashboard based on the role.
            if (role === 'admin') {
                navigate('/admin/dashboard');
            } else if (role === 'teacher') {
                navigate('/teacher/dashboard');
            } else {
                navigate('/student/dashboard');
            }
        } catch (err) {
            setError(err.message || "An error occurred. Please try again.");
        } finally {
            setLoading(false);
        }
    };  

  return (
        <div className='container'>
             <div className="login">
                <form className="form" onSubmit={handleSubmit}>
                    <p className="form-title">Sign in to your account</p>
                    {error && <div className="error-message">{error}</div>}
                
                    <div className="input-container">
                        <label htmlFor="email">Email</label>
                        <input 
                            type="email" 
                            id="email"
                            placeholder="Enter Email" 
                            value={email}       
                            onChange={(e) => { setEmail(e.target.value); setError(''); }} 
                            required
                        />
                    </div>

                    <div className="input-container">
                        <label htmlFor="password">Password</label>
                        <input 
                            type="password" 
                            id="password"
                            placeholder="Enter password" 
                            value={password} 
                            onChange={(e) => { setPassword(e.target.value); setError(''); }} 
                            required
                        />
                    </div>

                    <button type="submit" className="submit" disabled={loading}>
                        {loading ? 'Signing In...' : 'Sign In'}
                    </button>

                    <p className="signup-link">
                         No account? <Link to="/signup">Sign up</Link>
                    </p>
                </form>
            </div>
        </div>

  );
};
