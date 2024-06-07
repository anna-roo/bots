import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from trading_bot import fetch_ohlcv, moving_average, trading_strategy, execute_trade

class TestTradingBot(unittest.TestCase):

    @patch('ccxt.binance')
    def test_fetch_ohlcv(self, mock_binance):
        # Mock the response from the exchange
        mock_binance.return_value.fetch_ohlcv.return_value = [
            [1622548800000, 36000, 36100, 35900, 36050, 100],
            [1622548860000, 36050, 36200, 36000, 36100, 120],
        ]
        symbol = 'BTC/USDT'
        timeframe = '1m'
        data = fetch_ohlcv(symbol, timeframe)
        self.assertEqual(len(data), 2)
        self.assertEqual(data.columns.tolist(), ['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    
    def test_moving_average(self):
        data = pd.DataFrame({
            'close': [36000, 36050, 36100, 36150, 36200, 36250]
        })
        result = moving_average(data, 3)
        expected_result = pd.Series([np.nan, np.nan, 36050, 36100, 36150, 36200], name='close')
        pd.testing.assert_series_equal(result, expected_result)
    
    def test_trading_strategy(self):
        data = pd.DataFrame({
            'timestamp': [1, 2, 3, 4, 5, 6],
            'open': [36000, 36050, 36100, 36150, 36200, 36250],
            'high': [36100, 36200, 36250, 36300, 36350, 36400],
            'low': [35900, 36000, 36050, 36100, 36150, 36200],
            'close': [36000, 36050, 36100, 36150, 36200, 36250],
            'volume': [100, 120, 140, 160, 180, 200]
        })
        result = trading_strategy(data)
        self.assertEqual(result['signal'].iloc[-1], 1)
    
    @patch('ccxt.binance')
    def test_execute_trade(self, mock_binance):
        mock_exchange = mock_binance.return_value
        mock_exchange.fetch_balance.return_value = {
            'USDT': {'free': 1000},
            'BTC': {'free': 0}
        }
        
        # Mock the ohlcv data
        ohlcv = [
            [1622548800000, 36000, 36100, 35900, 36050, 100],
        ]
        
        execute_trade(1)  # Buy signal
        mock_exchange.create_market_buy_order.assert_called_once_with('BTC/USDT', 1000 / 36050)
        
        # Test Sell signal
        mock_exchange.fetch_balance.return_value = {
            'USDT': {'free': 0},
            'BTC': {'free': 1}
        }
        execute_trade(-1)  # Sell signal
        mock_exchange.create_market_sell_order.assert_called_once_with('BTC/USDT', 1)

if __name__ == '__main__':
    unittest.main()
