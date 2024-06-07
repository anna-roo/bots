import asyncio
from playwright.async_api import async_playwright
import ccxt
import pandas as pd
import numpy as np

async def fetch_ohlcv(symbol, timeframe):
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
    return pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

def moving_average(data, window):
    return data['close'].rolling(window=window).mean()

def trading_strategy(data):
    short_window = 5
    long_window = 20
    data['short_ma'] = moving_average(data, short_window)
    data['long_ma'] = moving_average(data, long_window)
    data['signal'] = 0
    data['signal'][short_window:] = np.where(
        data['short_ma'][short_window:] > data['long_ma'][short_window:], 1, 0
    )
    data['position'] = data['signal'].diff()
    return data

async def execute_trade(signal, page):
    if signal == 1:
        await page.click('#buy-button')  # Adjust the selector to match the actual web element
        print("Executed Buy Order")
    elif signal == -1:
        await page.click('#sell-button')  # Adjust the selector to match the actual web element
        print("Executed Sell Order")

async def test_trading_bot_functional():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.example-exchange.com/login")  # Replace with actual login URL

        # Log in to the exchange
        await page.fill('#username', 'your_username')  # Replace with actual username field selector
        await page.fill('#password', 'your_password')  # Replace with actual password field selector
        await page.click('#login-button')  # Replace with actual login button selector

        # Wait until login is complete
        await page.wait_for_selector('#account-balance')  # Adjust the selector to match the actual web element

        # Trading bot logic
        symbol = 'BTC/USDT'
        timeframe = '1m'
        ohlcv = await fetch_ohlcv(symbol, timeframe)
        data = trading_strategy(ohlcv)
        if data['position'].iloc[-1] == 1:
            await execute_trade(1, page)
        elif data['position'].iloc[-1] == -1:
            await execute_trade(-1, page)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_trading_bot_functional())
