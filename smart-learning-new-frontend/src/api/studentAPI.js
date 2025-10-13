import { authAPI as api } from './authAPI';

export const studentAPI = {
  getStudents: async ({ page = 1, limit = 10, search = '', role = 'student' }) => {
    const params = new URLSearchParams({ page, limit, role });
    if (search) {
      params.append('search', search);
    }
    return api.get(`/admin/users?${params.toString()}`);
  },

  addStudent: async (studentData) => {
    return api.post('/admin/users', { ...studentData, role: 'student' });
  },

  updateStudent: async (studentId, studentData) => {
    return api.put(`/admin/users/${studentId}`, studentData);
  },

  deleteStudent: async (studentId) => {
    return api.delete(`/admin/users/${studentId}`);
  },
};

// We need to add post, put, and delete methods to our authAPI

/**
 * In `src/api/authAPI.js`, add the following methods:
 *
 *  post: async (endpoint, data) => {
 *    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
 *      method: 'POST',
 *      headers: { 'Content-Type': 'application/json' },
 *      credentials: 'include',
 *      body: JSON.stringify(data),
 *    });
 *    return handleResponse(response);
 *  },
 *
 *  put: async (endpoint, data) => {
 *    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
 *      method: 'PUT',
 *      headers: { 'Content-Type': 'application/json' },
 *      credentials: 'include',
 *      body: JSON.stringify(data),
 *    });
 *    return handleResponse(response);
 *  },
 *
 *  delete: async (endpoint) => {
 *    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
 *      method: 'DELETE',
 *      credentials: 'include',
 *    });
 *    return handleResponse(response);
 *  },
 */