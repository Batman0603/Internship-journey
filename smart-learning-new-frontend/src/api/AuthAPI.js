const API_BASE_URL = 'http://127.0.0.1:5000';

export const authAPI = {
  login: async (email, password) => { // Changed parameter name for clarity
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }), // Changed 'username' to 'email' to match backend
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ message: 'Invalid Username or Password' }));
      throw new Error(errorData.message || 'Invalid Username or Password');
    }

    return response.json();
  },

  signup: async (username, email, password, role) => {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        email,
        password,
        role: role.toLowerCase(),
      }),
    });

    if (!response.ok) {
      let errorData;
      try {
        errorData = await response.json();
      } catch (e) {
        errorData = { message: 'An unknown registration error occurred.' };
      }
      throw new Error(errorData.message || 'Registration failed');
    }

    return response.json();
  },
};
