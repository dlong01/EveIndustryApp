import requests

# API ENDPOINTS
ESI_MARKET_PRICE = 'https://esi.evetech.net/latest/markets/prices/'

def get_adjusted_market_price(type_id):
    response = requests.get(ESI_MARKET_PRICE)
    prices = response.json()

    return prices[type_id]['adjusted_price']