/**
 * Определения типов TypeScript для приложения.
 * Определяет интерфейсы для ответов API и состояния приложения.
 */

export interface Coin {
  id: number;
  symbol: string;
  price: number;
  volume_24h: number | null;
  price_change_24h: number | null;
  price_change_percent_24h: number | null;
  high_24h: number | null;
  low_24h: number | null;
  funding_rate: number | null;
  open_interest: number | null;
  created_at: string;
  updated_at: string | null;
}

export interface FuturesHistory {
  id: number;
  symbol: string;
  price: number;
  previous_price: number | null;
  price_change: number | null;
  price_change_percent: number | null;
  volume: number | null;
  timestamp: string;
}

export interface PaginatedFuturesHistory {
  items: FuturesHistory[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface FuturesHistoryFilter {
  symbol?: string;
  min_percent_change?: number;
  max_percent_change?: number;
  start_time?: string;
  end_time?: string;
  page: number;
  page_size: number;
}
