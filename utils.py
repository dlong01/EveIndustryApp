EVE_DATABASE_PATH = './data/eve.db'

WAREHOUSE_DATABASE_PATH = './data/warehouse.db'
PREV_TRANS_PATH = './data/prev_transaction.txt'

ELDJ_SYSTEM_ID = 30003462

facility_eff = 1

def calculate_matt_efficiency(mat_eff):
    return facility_eff * (1-mat_eff)


