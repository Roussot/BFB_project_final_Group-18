/**
 * API Client for Agrimarket Flask Backend
 * Provides a clean interface for frontend-backend communication
 * @module api
 */

const API_BASE_URL = 'http://localhost:5000/api';

/**
 * Generic API call helper with error handling
 * @param {string} endpoint - API endpoint path
 * @param {Object} options - Fetch options (method, body, headers, etc.)
 * @returns {Promise} JSON response data
 * @throws {Error} If API request fails
 */
async function apiCall(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'API request failed' }));
      throw new Error(error.error || `HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
}

// Users API
const UsersAPI = {
  getAll: () => apiCall('/users'),
  getById: (id) => apiCall(`/users/${id}`),
  create: (userData) => apiCall('/users', {
    method: 'POST',
    body: JSON.stringify(userData)
  }),
  update: (id, userData) => apiCall(`/users/${id}`, {
    method: 'PUT',
    body: JSON.stringify(userData)
  })
};

// Stock API
const StockAPI = {
  getAll: (filters = {}) => {
    const params = new URLSearchParams(filters);
    return apiCall(`/stock?${params}`);
  },
  getById: (id) => apiCall(`/stock/${id}`),
  create: (stockData) => apiCall('/stock', {
    method: 'POST',
    body: JSON.stringify(stockData)
  }),
  update: (id, stockData) => apiCall(`/stock/${id}`, {
    method: 'PUT',
    body: JSON.stringify(stockData)
  })
};

// Orders API
const OrdersAPI = {
  getAll: (filters = {}) => {
    const params = new URLSearchParams(filters);
    return apiCall(`/orders?${params}`);
  },
  getById: (id) => apiCall(`/orders/${id}`),
  create: (orderData) => apiCall('/orders', {
    method: 'POST',
    body: JSON.stringify(orderData)
  }),
  update: (id, orderData) => apiCall(`/orders/${id}`, {
    method: 'PUT',
    body: JSON.stringify(orderData)
  })
};

// Logistics API
const LogisticsAPI = {
  getAll: () => apiCall('/logistics'),
  create: (logisticsData) => apiCall('/logistics', {
    method: 'POST',
    body: JSON.stringify(logisticsData)
  }),
  update: (id, logisticsData) => apiCall(`/logistics/${id}`, {
    method: 'PUT',
    body: JSON.stringify(logisticsData)
  })
};

// Analytics API
const AnalyticsAPI = {
  getKPIs: () => apiCall('/analytics/kpis')
};
