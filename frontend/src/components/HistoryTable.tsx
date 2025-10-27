/** Таблица истории */

import React from 'react';
import { FuturesHistory } from '../types';
import { format } from 'date-fns';

interface HistoryTableProps {
  data: FuturesHistory[];
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

const HistoryTable: React.FC<HistoryTableProps> = ({
  data,
  currentPage,
  totalPages,
  onPageChange,
}) => {
  const formatTimestamp = (timestamp: string) => {
    return format(new Date(timestamp), 'dd.MM.yyyy HH:mm:ss');
  };

  const formatPercent = (value: number | null) => {
    if (value === null || value === undefined) return 'N/A';
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(9)}%`;
  };

  const getPercentClass = (value: number | null) => {
    if (!value) return '';
    return value >= 0 ? 'positive' : 'negative';
  };

  return (
    <div className="history-table-container">
      {data.length === 0 ? (
        <div className="empty-state">
          <p>Нажмите "Найти" для отображения данных</p>
        </div>
      ) : (
        <>
          <table className="history-table">
            <thead>
              <tr>
                <th>Символ</th>
                <th>Цена</th>
                <th>Предыдущая цена</th>
                <th>Изменение</th>
                <th>Изменение %</th>
                <th>Время</th>
              </tr>
            </thead>
            <tbody>
              {data.map((item) => (
                <tr key={item.id}>
                  <td className="symbol-cell">{item.symbol}</td>
                  <td>${item.price.toFixed(8)}</td>
                  <td>
                    {item.previous_price
                      ? `$${item.previous_price.toFixed(8)}`
                      : 'N/A'}
                  </td>
                  <td className={getPercentClass(item.price_change)}>
                    {item.price_change
                      ? `$${item.price_change.toFixed(8)}`
                      : 'N/A'}
                  </td>
                  <td className={getPercentClass(item.price_change_percent)}>
                    {formatPercent(item.price_change_percent)}
                  </td>
                  <td className="timestamp-cell">
                    {formatTimestamp(item.timestamp)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {totalPages > 1 && (
            <div className="pagination">
              <button
                className="pagination-btn"
                onClick={() => onPageChange(currentPage - 1)}
                disabled={currentPage === 1}
              >
                ← Предыдущая
              </button>
              <span className="pagination-info">
                Страница {currentPage} из {totalPages}
              </span>
              <button
                className="pagination-btn"
                onClick={() => onPageChange(currentPage + 1)}
                disabled={currentPage === totalPages}
              >
                Следующая →
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default HistoryTable;
