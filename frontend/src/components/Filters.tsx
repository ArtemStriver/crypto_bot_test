/** Фильтры */

import React, { useState, useEffect } from 'react';
import { FuturesHistoryFilter } from '../types';

interface FiltersProps {
  onFilter: (filters: FuturesHistoryFilter) => void;
  symbolQuery?: string;
}

const Filters: React.FC<FiltersProps> = ({ onFilter, symbolQuery }) => {
  const [symbol, setSymbol] = useState<string>('');
  const [minPercent, setMinPercent] = useState<string>('');
  const [maxPercent, setMaxPercent] = useState<string>('');
  const [startTime, setStartTime] = useState<string>('');
  const [endTime, setEndTime] = useState<string>('');

  useEffect(() => {
    if (symbolQuery) {
      setSymbol(symbolQuery);
    }
  }, [symbolQuery]);

  const handleSearch = () => {
    const filters: FuturesHistoryFilter = {
      page: 1,
      page_size: 50,
    };

    if (symbol) {
      filters.symbol = symbol;
    }

    if (minPercent) {
      filters.min_percent_change = parseFloat(minPercent);
    }

    if (maxPercent) {
      filters.max_percent_change = parseFloat(maxPercent);
    }

    if (startTime) {
      filters.start_time = new Date(startTime).toISOString();
    }

    if (endTime) {
      filters.end_time = new Date(endTime).toISOString();
    }

    onFilter(filters);
  };

  return (
    <div className="filters-panel">
      <h3 className="filters-title">Фильтры</h3>

      <div className="filter-group">
        <label className="filter-label">Поиск по монете</label>
        <input
          type="text"
          placeholder="Например: BTC, ETH..."
          value={symbol}
          onChange={(e) => setSymbol(e.target.value.toUpperCase())}
          className="filter-input"
        />
        <small className="filter-hint">Введите символ монеты для фильтрации</small>
      </div>

      <div className="filter-group">
        <label className="filter-label">Разница в процентах</label>
        <div className="filter-row">
          <input
            type="number"
            step="0.01"
            placeholder="Минимум"
            value={minPercent}
            onChange={(e) => setMinPercent(e.target.value)}
            className="filter-input"
          />
          <span className="filter-separator">—</span>
          <input
            type="number"
            step="0.01"
            placeholder="Максимум"
            value={maxPercent}
            onChange={(e) => setMaxPercent(e.target.value)}
            className="filter-input"
          />
        </div>
      </div>

      <div className="filter-group">
        <label className="filter-label">Временной диапазон</label>
        <input
          type="datetime-local"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          className="filter-input"
          placeholder="Начало"
        />
        <input
          type="datetime-local"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
          className="filter-input"
          placeholder="Конец"
        />
      </div>

      <button className="btn btn-search" onClick={handleSearch}>
        Найти
      </button>
    </div>
  );
};

export default Filters;
