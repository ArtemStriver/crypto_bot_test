/** Заголовок */

import React from 'react';

interface HeaderProps {
  onMenuToggle: () => void;
  searchQuery: string;
  onSearchChange: (value: string) => void;
  onSearch: () => void;
}

const Header: React.FC<HeaderProps> = ({
  onMenuToggle,
  searchQuery,
  onSearchChange,
  onSearch,
}) => {
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      onSearch();
    }
  };

  return (
    <header className="header">
      <button className="mobile-menu-btn" onClick={onMenuToggle}>
        ☰
      </button>
      <div className="header-content">
        <h1 className="header-title">Криптобот - Мониторинг Фьючерсов</h1>
        <div className="search-box">
          <input
            type="text"
            placeholder="Поиск по монетам (например: BTC, ETH)..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            onKeyPress={handleKeyPress}
            className="search-input"
          />
          <button className="btn btn-search-inline" onClick={onSearch}>
             Найти
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
