/** API сервис */

import axios from 'axios';
import { Coin, PaginatedFuturesHistory, FuturesHistoryFilter } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  searchCoins: async (query?: string, limit = 100): Promise<Coin[]> => {
    const response = await api.get<Coin[]>('/coins/', {
      params: { query, limit },
    });
    return response.data;
  },

  filterFuturesHistory: async (
    filters: FuturesHistoryFilter
  ): Promise<PaginatedFuturesHistory> => {
    const response = await api.post<PaginatedFuturesHistory>(
      '/futures-history/filter',
      filters
    );
    return response.data;
  },
};

export default apiService;
