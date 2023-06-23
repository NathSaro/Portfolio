# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 17:25:14 2022

@author: Nathan SAROBERT
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from pandas_datareader import data as pdr
import yfinance as yf

#data importation and calculation of returns, mean return, correlation matix and covariance matrix
def get_data(stocks, start, end):
    stockData = yf.download(stocks, start=start, end=end)
    stockData = stockData['Close'] #We only take the close prices
    returns = stockData.pct_change()
    print(returns)
    returns.to_excel("test.xls")
    correlation = pd.DataFrame(returns)
    cor_mat = correlation.corr()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return meanReturns, covMatrix, returns, cor_mat

stockList = ['MC.PA', 'SGO.PA', 'RI.PA'] #We get the tickers, MC = LVMH
weights = np.array([0.3340, 0.3318, 0.3342])
endDate = dt.date(2022, 10, 20)
startDate = endDate - dt.timedelta(days=352)#We get the correct time frame
teta = np.array([3, -48, 11])


meanReturns, covMatrix, returns, cor_mat = get_data(stockList, startDate, endDate)

print("Covariance matrix:")
print(covMatrix)
print("correlation matrix:")
print(cor_mat)

#Monte-carlo simulation

mc_sim = 100 #number of simulations
T = 100 #time range in days

meanM = np.full(shape=(T, len(weights)), fill_value=meanReturns)
meanM = meanM.T

portfolio_sims = np.full(shape=(T, mc_sim), fill_value=0.0)

initialPortfolio = 5672.19 #our portfolio nominal

for m in range(0, mc_sim):
    Z = np.random.normal(size=(T, len(weights))) #take a bunch of uncorrelated sample data that we sample from a normal distribution and we corrate them with the CovMatrix
    L = np.linalg.cholesky(covMatrix)
    dailyReturns = meanM + np.inner(L, Z)
    portfolio_sims[:,m] = np.cumprod(np.inner(weights, dailyReturns.T)+1)*initialPortfolio

plt.plot(portfolio_sims)
plt.ylabel('portfolio Value (in Euro)')
plt.xlabel('Days')
plt.title('Monte Carlo simulation of our portfolio')
plt.show()
