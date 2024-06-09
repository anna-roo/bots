# Trading BOT # 

## [About the Trading BOT](../.README.MD)
## [Unit Test](../.Unit Test)
## [Functional Test](../.README.MD)
## [Playwright for Automated Testing of a Trading Bot](../.README.MD)


## About the Trading BOT
This is a simple trading bot script using Python and the ccxt library, which is commonly used for cryptocurrency trading. 
This bot will connect to a cryptocurrency exchange, fetch market data, and execute trades based on a simple moving average crossover strategy.
### Source file: Bot_tradingSimple.py 

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
### Running the Unit Test
python Bot_tradingSimpleUnitTest.py
## Functional Test
### Source file: Bot_tradingFunctionalTestCases.xlsx
To verify the overall functionality of the trading bot, ensuring it can connect to the exchange, fetch market data, apply the trading strategy, and execute trades correctly.
## Functional Test Script Implementation
### Source file: Bot_tradingSimpleFunctionalTest.py
### Explanation of the Functional Test Script
1.	Configuration:
The test configures the trading bot with mock API credentials and sets the parameters.
2.	Initialization:
Mocks the initialization of the exchange.
3.	Fetch OHLCV Data:
The test mocks the fetch_ohlcv method to return predefined OHLCV data.
4.	Apply Trading Strategy:
Applies the moving average crossover strategy to the fetched data.
5.	Check Signals:
Verifies that the generated signals are correct.
6.	Execute Trade:
Mocks the execution of a trade based on the generated signal and verifies the order was placed correctly.
7.	Fetch Balance After Trade:
Verifies that the balance reflects the executed trade.
8.	Repeat for Sell Signal:
Mocks the execution of a sell trade and verifies the order was placed correctly.
9.	Fetch Balance After Sell Trade:
Verifies that the balance reflects the executed trade.
10.	Verify Continuous Running:
Mocks the time.sleep method to avoid actual delays and verifies the bot can run continuously, fetching new data, applying the strategy, and executing trades in a loop
## Playwright for Automated Testing of a Trading Bot
### Source file: Bot_tradingSimplePlaywright.py
Using Playwright to run an automated Python script to test a trading bot involves setting up Playwright for browser automation and integrating it with your trading bot logic. Playwright provides powerful tools to automate web interactions, which can be very useful for testing web-based components of your trading bot.
#### Install Required Libraries
First, install Playwright and other necessary libraries: - pip install playwright ccxt pandas numpy.  After installing Playwright, iyou need to install it again to nstall the browsers: - playwright install
###Explanation
1.	Playwright Setup:
    - The script starts by launching a Playwright instance and opening a new browser page.
    - The browser navigates to the exchange's login page.
    - It logs in by filling in the username and password fields and submitting the form.
    - It waits until the login is complete by checking for a specific element that appears only after logging in (e.g., account balance).
2.	Trading Bot Functions:
    - Fetch OHLCV data, calculate moving averages, apply the trading strategy, and execute trades based on signals.
3.	Execute Trades via Web Interface:
    - The execute_trade function uses Playwright to click the buy or sell button based on the signal generated by the trading bot.
4.	Run the Test:
    - The script combines the trading bot logic with Playwright to run the test and execute trades.
    - It closes the browser after the test is complete.
5. Final Notes
    - Element Locators: Ensure that the CSS selectors (e.g., #username, #password,
#login-button, #account-balance, #buy-button, #sell-button) match the actual HTML structure of the exchange's web pages. You may need to inspect the web page to get the correct selectors.
    - Error Handling: Implement proper error handling and logging to deal with any issues that might occur during web interactions.
    - Security: Handle sensitive information (like usernames and passwords) securely, possibly using environment variables or a secure vault.

