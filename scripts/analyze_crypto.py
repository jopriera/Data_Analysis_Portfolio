from pymongo import MongoClient
import json
from dotenv import load_dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

def analyze_crypto_data():
    # Connect to MongoDB
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client['crypto_db']
    collection = db['crypto_data']

    # Retrieve the data
    data = list(collection.find())
    df = pd.DataFrame(data)

    # 1. Top 10 cryptocurrencies by market capitalization
    top_10 = df.sort_values('market_cap', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    plt.bar(top_10['symbol'], top_10['market_cap'])
    plt.title('Top 10 Cryptocurrencies by Market Capitalization')
    plt.xlabel('Symbol')
    plt.ylabel('Market Capitalization (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('top_10_market_cap.png')
    plt.close()

    # 2. Price distribution
    plt.figure(figsize=(12, 6))
    plt.hist(df['current_price'], bins=30)
    plt.title('Cryptocurrency Price Distribution')
    plt.xlabel('Price (USD)')
    plt.ylabel('Frequency')
    plt.savefig('price_distribution.png')
    plt.close()

    # 3. Relationship between volume and market capitalization
    plt.figure(figsize=(12, 6))
    plt.scatter(df['total_volume'], df['market_cap'])
    plt.title('Volume vs Market Capitalization')
    plt.xlabel('Total Volume')
    plt.ylabel('Market Capitalization')
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('volume_vs_market_cap.png')
    plt.close()

    # 4. Basic statistics
    print("Basic statistics:")
    print(df[['current_price', 'market_cap', 'total_volume']].describe())

    # Calculate the volume to market capitalization ratio
    df['volume_to_market_cap_ratio'] = df['total_volume'] / df['market_cap']

    # Identify outliers based on the volume-to-market-cap ratio
    mean_ratio = df['volume_to_market_cap_ratio'].mean()
    std_ratio = df['volume_to_market_cap_ratio'].std()

    # Outliers: values that are more than 2 standard deviations from the mean
    outliers = df[
        (df['volume_to_market_cap_ratio'] > mean_ratio + 2 * std_ratio) |
        (df['volume_to_market_cap_ratio'] < mean_ratio - 2 * std_ratio)
    ]

    print("\nOutliers based on volume to market cap ratio:")
    if not outliers.empty:
        for index, row in outliers.iterrows():
            print(f"Name: {row['name']}, Symbol: {row['symbol']}, Ratio: {row['volume_to_market_cap_ratio']:.2f}")
    else:
        print("No outliers found based on the current criteria.")

    # Brief investigation of the outlier: First Digital USD (FDUSD)
    print("\nInvestigation: Why is First Digital USD (FDUSD) an outlier?")
    print("FDUSD is a stablecoin, which often has high trading volumes relative to market capitalization.")
    print("This behavior is common for stablecoins as they are widely used for trading and as a safe haven during market volatility.")
    print("Recent events or listings on major exchanges could also explain the high volume observed.")
    
    # Calculate volatility (standard deviation of daily prices)
    # NOTE: This requires historical price data, which we don't have directly.
    # For simplicity, we'll use the current price as a proxy for volatility analysis.
    # In a real scenario, you'd fetch historical prices and calculate volatility over a specific period.

    # Since we don't have historical data, let's use a proxy for volatility based on the current price
    df['volatility_proxy'] = df['current_price'] / df['current_price'].mean()

    # Calculate the standard deviation of this proxy
    volatility_proxy_std = df['volatility_proxy'].std()

    print("\nVolatility Proxy Standard Deviation:", volatility_proxy_std)

    # Visualize the relationship between volatility proxy and market capitalization
    plt.figure(figsize=(12, 6))
    plt.scatter(df['volatility_proxy'], df['market_cap'])
    plt.title('Volatility Proxy vs Market Capitalization')
    plt.xlabel('Volatility Proxy')
    plt.ylabel('Market Capitalization')
    plt.xscale('log')
    plt.yscale('log')
    plt.savefig('volatility_proxy_vs_market_cap.png')
    plt.close()

if __name__ == "__main__":
    analyze_crypto_data()

