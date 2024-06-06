import ccxt
import time
import pandas as pd

# Configuration
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'
symbol = 'BTC/USDT'
timeframe = '1m'
short_window = 5
long_window = 20

# Initialize exchange
exchange = ccxt.binance({
    'apiKey': api_key,
    'secret': api_secret,
})

def fetch_ohlcv(symbol, timeframe):
    """Fetch OHLCV data from the exchange"""
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

def moving_average(data, window):
    """Calculate moving average"""
    return data['close'].rolling(window=window).mean()

def trading_strategy(data):
    """Simple Moving Average Crossover Strategy"""
    data['short_ma'] = moving_average(data, short_window)
    data['long_ma'] = moving_average(data, long_window)

    # Generate signals
    data['signal'] = 0
    data['signal'][short_window:] = np.where(
        data['short_ma'][short_window:] > data['long_ma'][short_window:], 1, 0
    )
    data['position'] = data['signal'].diff()

    return data

def execute_trade(signal):
    """Execute buy or sell order"""
    balance = exchange.fetch_balance()
    if signal == 1:
        # Buy signal
        amount = balance['USDT']['free'] / ohlcv[-1][4]  # Use all available USDT to buy BTC
        exchange.create_market_buy_order(symbol, amount)
        print(f"Bought {amount} BTC")
    elif signal == -1:
        # Sell signal
        amount = balance['BTC']['free']  # Use all available BTC to sell
        exchange.create_market_sell_order(symbol, amount)
        print(f"Sold {amount} BTC")

# Main loop
while True:
    ohlcv = fetch_ohlcv(symbol, timeframe)
    data = trading_strategy(ohlcv)

    if data['position'].iloc[-1] == 1:
        execute_trade(1)
    elif data['position'].iloc[-1] == -1:
        execute_trade(-1)

    time.sleep(60)  # Wait for 1 minute before fetching new data
