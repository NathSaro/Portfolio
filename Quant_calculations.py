# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 18:33:29 2023

@author: Nathan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt

# 1. Download market historical data for the period
start = dt.datetime(2018, 7, 3)
end = dt.datetime(2023, 6, 3)
market_ticker = "^FCHI"  # CAC40
stock_ticker = "MC.PA"  # LVMH


market_data = yf.download(market_ticker, start=start, end=end)
stock_data = yf.download(stock_ticker, start=start, end=end)


# 3. Plot market
market_data['Adj Close'].plot(title='CAC40 historical Price')
plt.show()
stock_data['Adj Close'].plot(title='LVMH historical Price')
plt.show()


# 4. Compute the overall market return over the period
market_return = (market_data['Adj Close'][-1] / market_data['Adj Close'][0]) - 1
print(f"Overall market return: {market_return:.2%}")

# 5. Compute market daily returns
market_daily_returns = market_data['Adj Close'].pct_change().dropna()

# 6. Compute the arithmetic daily mean and deviation from mean
market_mean = market_daily_returns.mean()
market_deviation = market_daily_returns - market_mean

# The following part is just to modify the X-axis legend, since there are a lot of dates, i regrouped them by years instead for better readability

# Plot the bar chart
ax = market_deviation.plot(kind='bar', title='CAC40 Deviation from Mean', figsize=(12, 6))

# Get unique years from the index and their corresponding positions
unique_years = market_deviation.index.year.unique()
year_positions = [market_deviation.index[market_deviation.index.year == year][0] for year in unique_years]

# Set x-axis ticks and labels
ax.set_xticks([market_deviation.index.get_loc(pos) for pos in year_positions])
ax.set_xticklabels(unique_years)

# END OF THE X-AXIS MODIFICATION

plt.xlabel('Year')
plt.ylabel('Deviation from Mean')
plt.show()

# 8. Compute variance
market_variance = market_daily_returns.var()

# 9. Compute standard deviation
market_std = market_daily_returns.std()

# 10. Annualize variance and standard deviation
annual_market_variance = market_variance * 252
annual_market_std = market_std * np.sqrt(252)

# 11. Introduce single stock and compare metrics
stock_daily_returns = stock_data['Adj Close'].pct_change().dropna()
stock_mean = stock_daily_returns.mean()
stock_variance = stock_daily_returns.var()
stock_std = stock_daily_returns.std()

# 12. Plot stock and market daily returns on the same chart
plt.figure(figsize=(12, 6))
plt.plot(market_daily_returns, label='CAC40')
plt.plot(stock_daily_returns, label='LVMH')
plt.title('Market and Stock Daily Returns')
plt.legend()
plt.show()

# 13. Compute the variance/covariance matrix
cov_matrix = pd.concat([market_daily_returns, stock_daily_returns], axis=1).cov()

# 14. Compute correlation
correlation = market_daily_returns.corr(stock_daily_returns)


# 15. Compute Beta
beta = cov_matrix.iloc[0, 1] / market_variance

print(f"Market annualized variance: {annual_market_variance:.8f}")
print(f"Market annualized standard deviation: {annual_market_std:.4f}")
print(f"Stock mean: {stock_mean:.8f}")
print(f"Stock variance: {stock_variance:.8f}")
print(f"Stock standard deviation: {stock_std:.4f}")
print(f"Correlation: {correlation:.4f}")
print(f"Beta: {beta:.4f}")