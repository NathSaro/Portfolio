#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 10:41:50 2023

@author: nathan
"""

import yfinance as yf
    
while True: 
    
    ticker = yf.Ticker('BTC-EUR').info
    market_price = ticker['regularMarketPrice']
    print('Market Price:', market_price)
    if market_price > 16763:
        print("Buy")
    elif market_price == 16763:
        print("Hold")
    else:
        print("Sell")
