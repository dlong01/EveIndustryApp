import requests

# API ENDPOINTS
ESI_MARKET_PRICE = 'https://esi.evetech.net/latest/markets/prices/'

market_prices_cache = None

def get_adjusted_market_price(type_id):
    if market_prices_cache == None:
        get_market_prices()

    adj_price = market_prices_cache[type_id][0]
    if adj_price == None:
        print(f"Error: No adjusted price found for item {type_id}")
        return -1
    else:
        return adj_price
    
def get_average_market_price(type_id):
    if market_prices_cache == None:
        get_market_prices()

    avg_price = market_prices_cache[type_id][1]
    if avg_price == None:
        print(f"Error: No adjusted price found for item {type_id}")
        return -1
    else:
        return avg_price

def get_market_prices():
    global market_prices_cache
    response = requests.get(ESI_MARKET_PRICE)
    prices_list = response.json()
    market_prices_cache = {
        item['type_id']: [
            item.get('adjusted_price', None), 
            item.get('average_price',None)
        ]
        for item in prices_list}
    return market_prices_cache

system_cost_index_cache = None

def get_system_cost_index(system_id):
    if system_cost_index_cache == None:
        get_system_cost_indicies()

    cost_index = system_cost_index_cache[system_id][0]['cost_index']
    return cost_index

def get_system_cost_indicies():
    global system_cost_index_cache
    response = requests.get('https://esi.evetech.net/latest/industry/systems/')
    system_cost_index_cache = {
        item['solar_system_id']: item['cost_indices']
        for item in response.json()}
    return system_cost_index_cache