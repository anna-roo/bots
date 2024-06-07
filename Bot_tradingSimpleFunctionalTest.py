import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from trading_bot import fetch_ohlcv, moving_average, trading_strategy, execute_trade

class TestTradingBotFunctional(unittest.TestCase):

    @patch('ccxt.binance')
    def test_trading_bot_functional(self, mock_binance):
        # Step 1: Configure the trading bot
        api_key = 'test_api_key'
        api_secret = 'test_api_secret'
        symbol = 'BTC/USDT'
        timeframe = '1m'
        short_window = 5
        long_window = 20

        # Initialize exchange
        exchange = mock_binance.return_value
        exchange.apiKey = api_key
        exchange.secret = api_secret
        
        # Step 3: Fetch OHLCV data
        exchange.fetch_ohlcv.return_value = [
            [1622548800000, 36000, 36100, 35900, 36050, 100],
            [1622548860000, 36050, 36200, 36000, 36100, 120],
            [1622548920000, 36100, 36250, 36050, 36150, 140],
            [1622548980000, 36150, 36300, 36100, 36200, 160],
            [1622549040000, 36200, 36350, 36150, 36250, 180],
            [1622549100000, 36250, 36400, 36200, 36300, 200],
        ]
        ohlcv = fetch_ohlcv(symbol, timeframe)
        self.assertEqual(len(ohlcv), 6)
        
        # Step 4: Apply trading strategy
        data = trading_strategy(ohlcv)
        
        # Step 5: Check the signals
        self.assertEqual(data['signal'].iloc[-1], 1)  # Assuming a buy signal
        
        # Step 6: Execute trade based on signal
        exchange.fetch_balance.return_value = {
            'USDT': {'free': 1000},
            'BTC': {'free': 0}
        }
        execute_trade(1)  # Buy signal
        exchange.create_market_buy_order.assert_called_once_with('BTC/USDT', 1000 / 36300)
        
        # Step 7: Fetch balance after trade
        balance_after_buy = exchange.fetch_balance()
        self.assertEqual(balance_after_buy['USDT']['free'], 0)
        
        # Step 8: Repeat for sell signal
        exchange.fetch_balance.return_value = {
            'USDT': {'free': 0},
            'BTC': {'free': 1}
        }
        execute_trade(-1)  # Sell signal
        exchange.create_market_sell_order.assert_called_once_with('BTC/USDT', 1)
        
        # Step 9: Fetch balance after sell trade
        balance_after_sell = exchange.fetch_balance()
        self.assertEqual(balance_after_sell['BTC']['free'], 0)
        
        # Step 10: Verify continuous running (mocking time.sleep to avoid actual delay)
        with patch('time.sleep', return_value=None):
            for _ in range(3):
                ohlcv = fetch_ohlcv(symbol, timeframe)
                data = trading_strategy(ohlcv)
                if data['position'].iloc[-1] == 1:
                    execute_trade(1)
                elif data['position'].iloc[-1] == -1:
                    execute_trade(-1)

if __name__ == '__main__':
    unittest.main()
