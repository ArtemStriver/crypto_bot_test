/** Список монет */

import React from 'react';
import { Coin } from '../types';

interface CoinsListProps {
  coins: Coin[];
}

const CoinsList: React.FC<CoinsListProps> = ({ coins }) => {
  const formatPrice = (price: number) => {
    return `$${price.toFixed(9)}`;
  };

  const formatPercent = (value: number | null) => {
    if (value === null) return 'N/A';
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(9)}%`;
  };

  const getPercentClass = (value: number | null) => {
    if (!value) return '';
    return value >= 0 ? 'positive' : 'negative';
  };

  return (
    <div className="coins-list">
      {coins.length === 0 ? (
        <div className="empty-state">
          <p>Монеты не найдены</p>
        </div>
      ) : (
        coins.map((coin) => (
          <div key={coin.id} className="coin-card">
            <div className="coin-header">
              <h3 className="coin-symbol">{coin.symbol}</h3>
              <span className="coin-price">{formatPrice(coin.price)}</span>
            </div>
            <div className="coin-details">
              <div className="detail-item">
                <span className="detail-label">24ч изменение:</span>
                <span
                  className={`detail-value ${getPercentClass(
                    coin.price_change_percent_24h
                  )}`}
                >
                  {formatPercent(coin.price_change_percent_24h)}
                </span>
              </div>
              {coin.volume_24h && (
                <div className="detail-item">
                  <span className="detail-label">Объем 24ч:</span>
                  <span className="detail-value">
                    ${coin.volume_24h.toLocaleString()}
                  </span>
                </div>
              )}
              {coin.funding_rate !== null && (
                <div className="detail-item">
                  <span className="detail-label">Funding Rate:</span>
                  <span className="detail-value">
                    {(coin.funding_rate * 100).toFixed(8)}%
                  </span>
                </div>
              )}
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default CoinsList;
