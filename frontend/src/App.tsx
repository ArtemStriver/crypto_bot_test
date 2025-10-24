/** Главный компонент */

import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Filters from './components/Filters';
import HistoryTable from './components/HistoryTable';
import CoinsList from './components/CoinsList';
import apiService from './services/api';
import { Coin, FuturesHistory, FuturesHistoryFilter } from './types';
import './styles/App.css';

const App: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeView, setActiveView] = useState<'coins' | 'history'>('coins');
  const [searchQuery, setSearchQuery] = useState('');
  const [coins, setCoins] = useState<Coin[]>([]);
  const [historyData, setHistoryData] = useState<FuturesHistory[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const [historySearched, setHistorySearched] = useState(false);
  const [lastFilters, setLastFilters] = useState<FuturesHistoryFilter | null>(null);

  useEffect(() => {
    loadCoins();
  }, []);

  const loadCoins = async (query?: string) => {
    try {
      setLoading(true);
      const data = await apiService.searchCoins(query, 100);
      setCoins(data);
    } catch (error) {
      console.error('Error loading coins:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (activeView === 'coins') {
      loadCoins(searchQuery);
    } else if (activeView === 'history') {
      const filters: FuturesHistoryFilter = {
        page: 1,
        page_size: 50,
      };
      if (searchQuery) {
        filters.symbol = searchQuery.toUpperCase();
      }
      handleFilter(filters);
    }
  };

  const handleFilter = async (filters: FuturesHistoryFilter) => {
    try {
      setLoading(true);
      setHistorySearched(true);
      setLastFilters(filters);
      const response = await apiService.filterFuturesHistory(filters);
      setHistoryData(response.items);
      setCurrentPage(response.page);
      setTotalPages(response.total_pages);
    } catch (error) {
      console.error('Error filtering history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = async (page: number) => {
    try {
      setLoading(true);
      const filters: FuturesHistoryFilter = lastFilters
        ? { ...lastFilters, page }
        : { page, page_size: 50 };

      const response = await apiService.filterFuturesHistory(filters);
      setHistoryData(response.items);
      setCurrentPage(response.page);
      setTotalPages(response.total_pages);
    } catch (error) {
      console.error('Error changing page:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewChange = (view: 'coins' | 'history') => {
    setActiveView(view);
    if (view === 'coins') {
      setSearchQuery('');
    } else {
      setHistorySearched(false);
    }
  };

  return (
    <div className="app">
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        activeView={activeView}
        onViewChange={handleViewChange}
      />

      <main className="main-content">
        <Header
          onMenuToggle={() => setSidebarOpen(true)}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          onSearch={handleSearch}
        />

        <div className="content-container">
          {activeView === 'history' && (
            <Filters onFilter={handleFilter} symbolQuery={searchQuery} />
          )}

          <div className="content-area">
            {loading && <div className="loading">Загрузка...</div>}

            {!loading && activeView === 'coins' && (
              <div className="section">
                <h2 className="section-title">
                  Фьючерсы Binance {searchQuery && `- Поиск: ${searchQuery}`}
                </h2>
                <CoinsList coins={coins} />
              </div>
            )}

            {!loading && activeView === 'history' && (
              <div className="section">
                <h2 className="section-title">
                  История изменений фьючерсов {searchQuery && `- ${searchQuery}`}
                </h2>
                <HistoryTable
                  data={historyData}
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={handlePageChange}
                />
                {!historySearched && (
                  <div className="info-message">
                    Введите символ монеты в поиске сверху или используйте фильтры слева и нажмите "Найти"
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default App;
