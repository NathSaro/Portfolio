#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 16:51:53 2023

@author: nathan
"""

import requests
import re
import yfinance as yf

# URL for the LVMH financial data
ticker = "MC.PA"
url = f"https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}"

# Send a request to the website and retrieve the data
response = requests.get(url)
data = response.text

# Extract the relevant financial data
start = data.find('Free Cash Flow')
end = data.find('Total Debt', start)
data = data[start:end].strip()
free_cash_flow_string = re.search(r'>([\d,]+)<', data).group(1)
free_cash_flow = int(free_cash_flow_string.replace(',', ''))
market_price = float(yf.Ticker(ticker).info['regularMarketPrice'])

try:
    revenue = int(re.search(r'\d+', financials['Total Revenue']['Annual']).group())
except (AttributeError, TypeError):
    print("Could not extract revenue data.")
    revenue = None


# Perform the DCF analysis
discount_rate = 0.05
years = 10
discounted_cash_flow = 0
for i in range(years):
    discounted_cash_flow += free_cash_flow / ((1 + discount_rate) ** i)

# Calculate the intrinsic value
intrinsic_value = discounted_cash_flow / (1 + discount_rate) ** years

# Compare the intrinsic value to the market price
if intrinsic_value > market_price:
    print(f"The intrinsic value of {ticker} is {intrinsic_value}, which is higher than the market price of {market_price}. This may indicate that the stock is undervalued.")
else:
    print(f"The intrinsic value of {ticker} is {intrinsic_value}, which is lower than the market price of {market_price}. This may indicate that the stock is overvalued.")
