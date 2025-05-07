import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';
console.log('API URL:', API_URL);

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true
});

// Add a request interceptor to add the auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
      console.log('API Request: Adding token to headers');
    } else {
      console.log('API Request: No token found in localStorage');
    }
    console.log('API Request:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      fullUrl: `${API_URL}${config.url}`
    });
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add a response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', {
      url: response.config.url,
      status: response.status,
      data: response.data,
      fullUrl: `${API_URL}${response.config.url}`
    });
    return response;
  },
  (error) => {
    console.error('API Response Error:', {
      url: error.config?.url,
      status: error.response?.status,
      data: error.response?.data,
      message: error.message,
      fullUrl: error.config ? `${API_URL}${error.config.url}` : 'unknown'
    });
    return Promise.reject(error);
  }
);

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData extends LoginCredentials {
  name: string;
}

export interface User {
  id: number;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  user: User;
}

export const authService = {
  async login(credentials: LoginCredentials) {
    console.log('Auth Service: Attempting login...');
    const response = await api.post<LoginResponse>('/auth/login', credentials);
    console.log('Auth Service: Login response:', response.data);
    
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
      console.log('Auth Service: Token stored');
    } else {
      console.error('Auth Service: No token in response');
    }
    
    return response.data;
  },

  async register(data: RegisterData) {
    console.log('Auth Service: Attempting registration...');
    const response = await api.post('/auth/register', data);
    console.log('Auth Service: Registration response:', response.data);
    return response.data;
  },

  async getCurrentUser() {
    console.log('Auth Service: Fetching current user...');
    const token = localStorage.getItem('token');
    console.log('Auth Service: Current token:', token ? 'Present' : 'Missing');
    
    const response = await api.get<User>('/auth/me');
    console.log('Auth Service: Current user response:', response.data);
    return response.data;
  },

  logout() {
    console.log('Auth Service: Logging out...');
    localStorage.removeItem('token');
  },

  isAuthenticated() {
    const hasToken = !!localStorage.getItem('token');
    console.log('Auth Service: Checking authentication:', hasToken);
    return hasToken;
  },
};

export default api; 