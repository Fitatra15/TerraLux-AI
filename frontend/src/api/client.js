import axios from 'axios';

const API_BASE = '/api';
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes (F15-A)

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Intercepteur Auth JWT
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('terralux_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/**
 * Cached GET helper with 5 min localStorage caching (F15-A)
 */
export async function cachedGet(url, params = {}) {
  const cacheKey = `terralux_cache_${url}_${JSON.stringify(params)}`;
  const cached = localStorage.getItem(cacheKey);

  if (cached) {
    try {
      const parsed = JSON.parse(cached);
      if (Date.now() - parsed.timestamp < CACHE_TTL_MS) {
        return parsed.data;
      }
    } catch (e) {
      localStorage.removeItem(cacheKey);
    }
  }

  // Effectuer la requête réelle
  const response = await apiClient.get(url, { params });
  try {
    localStorage.setItem(cacheKey, JSON.stringify({
      timestamp: Date.now(),
      data: response.data
    }));
  } catch (e) {
    // Quota localStorage dépassé, ignorer
  }
  return response.data;
}

export default apiClient;
