EVE_DATABASE_PATH = './data/eve.db'
WAREHOUSE_DATABASE_PATH = './data/warehouse.db'
PREV_TRANS_PATH = './data/prev_transaction.txt'

facility_eff = 0.99

def calculate_matt_efficiency(mat_eff):
    return facility_eff * (1-mat_eff)