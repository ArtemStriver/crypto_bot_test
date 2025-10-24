"""Работа с Binance API"""

import httpx
from typing import List, Dict, Optional
from app.core.config import settings


class BinanceService:
    def __init__(self):
        self.base_url = settings.BINANCE_BASE_URL
        self.api_key = settings.BINANCE_API_KEY
        self.api_secret = settings.BINANCE_API_SECRET
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Закрыть соединение"""
        await self.client.aclose()

    async def get_all_futures_symbols(self) -> List[str]:
        """Получить все фьючерсные пары"""
        try:
            response = await self.client.get(f"{self.base_url}/fapi/v1/exchangeInfo")
            response.raise_for_status()
            data = response.json()

            symbols = [
                symbol_info["symbol"]
                for symbol_info in data.get("symbols", [])
                if symbol_info["status"] == "TRADING"
                and symbol_info["contractType"] == "PERPETUAL"
            ]

            return symbols

        except Exception as e:
            return []

    async def get_24h_ticker(self, symbol: Optional[str] = None) -> List[Dict]:
        """Данные за 24 часа"""
        try:
            url = f"{self.base_url}/fapi/v1/ticker/24hr"
            params = {"symbol": symbol} if symbol else {}

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Всегда возвращаем список
            if isinstance(data, dict):
                data = [data]

            return data

        except Exception as e:
            return []

    async def get_current_price(self, symbol: Optional[str] = None) -> List[Dict]:
        """Текущие цены"""
        try:
            url = f"{self.base_url}/fapi/v1/ticker/price"
            params = {"symbol": symbol} if symbol else {}

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                data = [data]

            return data

        except Exception as e:
            return []

    async def get_funding_rate(self, symbol: Optional[str] = None) -> List[Dict]:
        """Ставки финансирования"""
        try:
            url = f"{self.base_url}/fapi/v1/premiumIndex"
            params = {"symbol": symbol} if symbol else {}

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict):
                data = [data]

            return data

        except Exception as e:
            return []

    async def get_open_interest(self, symbol: str) -> Optional[Dict]:
        """Открытый интерес"""
        try:
            url = f"{self.base_url}/fapi/v1/openInterest"
            params = {"symbol": symbol}

            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            return data

        except Exception as e:
            return None

    async def get_complete_market_data(self) -> List[Dict]:
        """Собрать все данные по монетам"""
        try:
            # Получаем все тикеры (содержат большую часть нужных данных)
            tickers = await self.get_24h_ticker()

            # Получаем ставки финансирования для всех символов
            funding_rates = await self.get_funding_rate()
            funding_map = {item["symbol"]: item.get("lastFundingRate", 0) for item in funding_rates}

            # Объединяем данные
            complete_data = []
            for ticker in tickers:
                symbol = ticker["symbol"]
                complete_data.append({
                    "symbol": symbol,
                    "price": float(ticker.get("lastPrice", 0)),
                    "volume_24h": float(ticker.get("volume", 0)),
                    "price_change_24h": float(ticker.get("priceChange", 0)),
                    "price_change_percent_24h": float(ticker.get("priceChangePercent", 0)),
                    "high_24h": float(ticker.get("highPrice", 0)),
                    "low_24h": float(ticker.get("lowPrice", 0)),
                    "funding_rate": float(funding_map.get(symbol, 0)),
                    "open_interest": None,  # Пропускаем индивидуальные запросы OI для производительности
                })

            return complete_data

        except Exception as e:
            return []


# Singleton экземпляр
binance_service = BinanceService()
