import requests
import json

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false"
    response = requests.get(url)
    data = response.json()
    
    with open('data/crypto_data.json', 'w') as f:
        json.dump(data, f, indent=4)

fetch_crypto_data()

