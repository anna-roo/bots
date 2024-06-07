# Trading BOT # 
### Source file: Bot_tradingSimple.py 
This is a simple trading bot script using Python and the ccxt library, which is commonly used for cryptocurrency trading. 
This bot will connect to a cryptocurrency exchange, fetch market data, and execute trades based on a simple moving average crossover strategy.
### Explanation of the Trading BOT
#### 1.	Configuration:
api_key and api_secret: Your API credentials from the exchange.
symbol: The trading pair (e.g., BTC/USDT). timeframe: The timeframe for fetching OHLCV data (e.g., 1 minute).
short_window and long_window: The periods for the short and long moving averages. Note: - USDT is the symbol for Tether, a cryptocurrency that is pegged to the U.S. dollar. This means USDT is a stablecoin, fluctuating in value with the U.S. dollar
#### 2.	Initialize Exchange:
The script initializes the connection to the Binance exchange using the ccxt library with the provided API credentials.
#### 3.	Fetch OHLCV Data:
The fetch_ohlcv function fetches Open, High, Low, Close, and Volume (OHLCV) data for the specified trading pair and timeframe from the exchange.
#### 4.	Calculate Moving Average:
The moving_average function calculates the moving average of the closing prices over the specified window period.
#### 5.	Trading Strategy:
  The trading_strategy function implements a simple moving average crossover strategy. It calculates the short-term and long-term moving averages and generates buy/sell signals based on the crossover. If the short-term MA crosses above the long-term MA, a buy signal (1) is generated.
If the short-term MA crosses below the long-term MA, a sell signal (-1) is generated.
#### 6.	Execute Trade:
The execute_trade function places market buy or sell orders based on the generated signals.
If a buy signal is detected, it uses all available USDT to buy BTC.
If a sell signal is detected, it sells all available BTC.
#### 7.	Main Loop:
  The script runs an infinite loop where it fetches the latest OHLCV data, applies the trading strategy, and executes trades based on the generated signals.
  The script waits for 1 minute (time.sleep(60)) before fetching new data and repeating the process.
#### Note:
This is a basic example and should not be used for live trading without thorough testing and improvements. Real trading bots need more robust error handling, risk management, and should be backtested on historical data.

## Unit Test  
### Source file: Bot_tradingSimpleUnitTest.py
### Explanation of the Unit Test
The unit tests uses the unittest library in Python. 
The ccxt library methods are mocked to simulate the behavior of the exchange, ensuring our tests are not dependent on actual API calls. 
Install the necessary libraries: - pip install pandas numpy ccxt unittest mock
Explanation of the Unit Test Script

1.	Importing Libraries:
    - unittest for writing the tests.
    - patch and MagicMock from unittest.mock for mocking external dependencies. pandas and numpy for data manipulation and testing.
    - functions from the trading bot script (fetch_ohlcv, moving_average, trading_strategy, execute_trade).
2.	Test Class:
TestTradingBot is the main test class inheriting from unittest.TestCase.
3.	Test Methods:
    - test_fetch_ohlcv: Mocks the fetch_ohlcv method from ccxt to return predefined OHLCV data and checks the length and column names of the returned DataFrame.
    - test_moving_average: Tests the moving_average function to ensure it calculates the moving average correctly.
    - test_trading_strategy: Tests the trading_strategy function to ensure it generates the correct buy/sell signals.
    - test_execute_trade: Mocks the execute_trade function to test if it places the correct buy and sell orders based on the signals.
### Running the Tests
python Bot_tradingSimpleUnitTest.py
## Functional Test Script
### Source file: Bot_tradingFunctionalTestCases.xlsx
To verify the overall functionality of the trading bot, ensuring it can connect to the exchange, fetch market data, apply the trading strategy, and execute trades correctly.
