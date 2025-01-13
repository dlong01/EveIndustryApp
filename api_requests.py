import requests

# API ENDPOINTS
ESI_MARKET_PRICE = 'https://esi.evetech.net/latest/markets/prices/'

def get_adjusted_market_price():
    response = requests.get(ESI_MARKET_PRICE)
    print(response.json())