# Project Plan

## Title
Crypto Forecasting

## Main Question
1. How can we predict the future returns based on information of historic trades for several cryptoassets, such as Bitcoin and Ethereum.

## Description
Forecasting the cryptocurrency market is a difficult task due to its lack of regulation, extreme price volatility, complex technology, 
speculative behavior, potential illiquidity, and other external factors. This project begins with cleaning, feature engineering, and 
structuring the data for machine learning algorithms. The data is then used to forecast short-term returns in 14 popular cryptocurrencies.

## Datasources
Data source for this specific problem is Kaggle, a well-known platform for data science competitions and datasets.

### Datasource1: Kaggle
Data URL: 
*  Data URL : https://www.kaggle.com/competitions/g-research-crypto-forecasting/data?select=train.csv
*  Test and Train Data: Splitting the main data into train and test accordingly. 
*  Data Type: CSV

This dataset contains information on historic trades for several cryptoassets, such as Bitcoin and Ethereum. 
The training data csv file consist of following columns:
  timestamp - A timestamp for the minute covered by the row.
  Asset_ID - An ID code for the cryptoasset.
  Count - The number of trades that took place this minute.
  Open - The USD price at the beginning of the minute.
  High - The highest USD price during the minute.
  Low - The lowest USD price during the minute.
  Close - The USD price at the end of the minute.
  Volume - The number of cryptoasset units traded during the minute.
  VWAP - The volume weighted average price for the minute.
  Target - 15 minute residualized returns.
    
## Work Packages
    
1. Collect and refine the dataset.
2. Establish data pipelines for accessing the data. 
3. Implement testing for the pipeline.
4. Visualize the data.
5. Feature Engineering
6. Setup machine learning algorithm pipeline
7. Leverage GitHub Actions for continuous integration.
8. Draw conclusions, and compile a final report for the project. 
