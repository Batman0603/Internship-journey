const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";

/**
 * Helper function to handle fetch responses uniformly
 */
const handleResponse = async (response) => {
  // If server mistakenly returned HTML (index.html from Vite dev server), throw a helpful error
  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('text/html')) {
    const text = await response.text().catch(() => '');
    throw new Error('Expected JSON but received HTML. This usually means the API URL is incorrect or the backend is not running. Response snippet: ' + text.slice(0, 200));
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const message =
      errorData.error || errorData.message || "Something went wrong. Please try again.";
    throw new Error(message);
  }

  return response.json();
};

export const authAPI = {
  /**
   * Login user and store JWT in HttpOnly cookie (set by backend)
   */
  login: async (email, password) => {
    const url = `${API_BASE_URL}/api/auth/login`;
    // console.debug('authAPI.login ->', url);
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", // 🔥 Send & receive cookies (JWT HttpOnly)
      body: JSON.stringify({ email, password }),
    });

    return handleResponse(response);
  },

  /**
   * Register new user (backend sets JWT cookie on success)
   */
  signup: async (username, email, password, role) => {
    const url = `${API_BASE_URL}/api/auth/signup`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify({
        username,
        email,
        password,
        role: role.toLowerCase(),
      }),
    });

    return handleResponse(response);
  },

  /**
   * Logout user and clear JWT cookie
   */
  logout: async () => {
    const url = `${API_BASE_URL}/api/auth/logout`;
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });

    return handleResponse(response);
  },

  /**
   * GET request to protected routes
   */
  get: async (endpoint) => {
    const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : '/' + endpoint}`;
    // console.debug('authAPI.get ->', url);
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", // 🔥 Ensures JWT cookie is sent automatically
    });

    return handleResponse(response);
  },

  /**
   * POST request to protected routes
   */
  post: async (endpoint, data) => {
    const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : '/' + endpoint}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * PUT request to protected routes
   */
  put: async (endpoint, data) => {
    const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : '/' + endpoint}`;
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify(data),
    });
    return handleResponse(response);
  },

  /**
   * DELETE request to protected routes
   */
  delete: async (endpoint) => {
    const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : '/' + endpoint}`;
    const response = await fetch(url, {
      method: 'DELETE',
      credentials: 'include',
    });
    return handleResponse(response);
  },
};
