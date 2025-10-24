/** Боковая панель */

import React from 'react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  activeView: 'coins' | 'history';
  onViewChange: (view: 'coins' | 'history') => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose, activeView, onViewChange }) => {
  const handleViewClick = (view: 'coins' | 'history') => {
    onViewChange(view);
    if (window.innerWidth <= 768) {
      onClose();
    }
  };

  return (
    <>
      <aside className={`sidebar ${isOpen ? 'active' : ''}`}>
        <div className="sidebar-header">
          <h2 className="logo">CB</h2>
          <button className="close-btn" onClick={onClose}>
            &times;
          </button>
        </div>
        <nav className="nav-menu">
          <button
            className={`nav-item ${activeView === 'coins' ? 'active' : ''}`}
            onClick={() => handleViewClick('coins')}
          >
            <span className="nav-text">Монеты</span>
          </button>
          <button
            className={`nav-item ${activeView === 'history' ? 'active' : ''}`}
            onClick={() => handleViewClick('history')}
          >
            <span className="nav-text">История изменений</span>
          </button>
        </nav>
        <div className="sidebar-footer">
          <p className="sidebar-info">Обновление данных:</p>
          <p className="sidebar-info-small">• Монеты: каждую минуту</p>
          <p className="sidebar-info-small">• История: каждую секунду</p>
        </div>
      </aside>
      {isOpen && <div className="overlay" onClick={onClose}></div>}
    </>
  );
};

export default Sidebar;
