import math
import sqlite3
from utils import WAREHOUSE_DATABASE_PATH, EVE_DATABASE_PATH

def init_warehouse():
    conn = sqlite3.connect(WAREHOUSE_DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE items (typeID INTEGER PRIMARY KEY, quantity INTEGER, cost REAL);")
    conn.commit()

    cursor.execute("CREATE TABLE bpcLibrary (typeID INTEGER PRIMARY KEY, me INTEGER, te INTEGER, cost REAL);")
    conn.commit()

    conn.close()

def verify_warehouse():
    conn = sqlite3.connect(WAREHOUSE_DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if len(tables) == 0:
        print("Warehouse not found, creating warehouse...")
        init_warehouse()
        return False
    else:
        print("Warehouse found")
        return True
    
def update_warehouse():
    
    
def add_items(records):
    conn = sqlite3.connect(WAREHOUSE_DATABASE_PATH)
    cursor = conn.cursor()

    for record in records:
        cursor.execute("SELECT * FROM items WHERE typeID = ?", (record.typeID,))
        result = cursor.fetchone()
        if result:
            cursor.execute("SELECT quantity, cost FROM items WHERE typeID = ?", (record.typeID,))
            quanity_stored, cost_stored = cursor.fetchone()
            new_quantity = quanity_stored + record.quantity
            new_cost = ((cost_stored * quanity_stored) + (record.cost * record.quantity)) / new_quantity

            new_cost = math.ceil(new_cost * 100) / 100 # Round up to 2 decimal places

            cursor.execute("UPDATE items SET quantity = ?, cost = ? WHERE typeID = ?", (new_quantity, new_cost, record.typeID))
        else:
            cursor.execute("INSERT INTO items (typeID, quantity, cost) VALUES (?, ?, ?)", (record.typeID, record.quantity, record.cost))
        conn.commit()

    conn.close()

def remove_items(records):
    conn = sqlite3.connect(WAREHOUSE_DATABASE_PATH)
    cursor = conn.cursor()

    for record in records:
        cursor.execute("SELECT * FROM items WHERE typeID = ?", (record.typeID,))
        result = cursor.fetchone()
        if result:
            cursor.execute("SELECT quantity FROM items WHERE typeID = ?", (record.typeID,))
            quanity_stored = cursor.fetchone()
            new_quantity = quanity_stored - record.quantity
            if new_quantity < 0:
                print(f"Insufficient quantity of {record.typeID}")
                return
            elif new_quantity == 0:
                cursor.execute("DELETE FROM items WHERE typeID = ?", (record.typeID,))
            else:
                cursor.execute("UPDATE items SET quantity = ? WHERE typeID = ?", (new_quantity, record.typeID))
        else:
            print(f"Item not found: {record.typeID}")
        conn.commit()

    conn.close()

def parse_record(item_string):
    item_info = item_string.split("\t")
    type_id = convert_name_to_typeID(item_info[2])
    record = ''
    if not type_id:
        print(f"Item not found: {item_info[2]}")
    else:
        quantity = int(item_info[1])
        cost = float(item_info[3].replace(" ISK", ""))
        record = ItemRecord(type_id, quantity, cost)
    return record

def convert_name_to_typeID(name):
    conn = sqlite3.connect(EVE_DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT typeID FROM invTypes WHERE typeName = ?", (name,))
    typeID = cursor.fetchone()

    conn.close()

    if typeID:
        return typeID[0]
    else:
        return None
    
def input_items():
    option = input("Are you copying items from market transactions? (y/n): ")
    records = []
    if option.lower() == "y":
        records = get_market_transaction_items()
        update_warehouse(records)
    else:
        
        records = manual_input_items()

    

def get_market_transaction_items():
    print("Paste the items in below: \n")
    records = []
    while True:
        item_string = input()
        if item_string != "":
            records.append(parse_record(item_string))
        else:
            break
    return records

def manual_input_items():
    records = []
    cont = 'y'
    while cont != "n":
        name = input("Enter the item name: ")
        quantity = input("Enter the item quantity: ")
        cost = input("Enter the total cost: ")

        unit_price = float(cost) / int(quantity)
        type_id = convert_name_to_typeID(name)

        if not type_id:
            print(f"Item not found: {name}")
        else:
            records.append(ItemRecord(type_id, int(quantity), unit_price))
        
        cont = input("Do you want to add another item? (y/n): ")
    return records

def manual_remove_items():
    records = []
    cont = 'y'
    while cont != "n":
        name = input("Enter the item name: ")
        quantity = input("Enter the item quantity: ")

        unit_price = float(cost) / int(quantity)
        type_id = convert_name_to_typeID(name)

        if not type_id:
            print(f"Item not found: {name}")
        else:
            records.append(ItemRecord(type_id, int(quantity), unit_price))
        
        cont = input("Do you want to add another item? (y/n): ")
    return records

class ItemRecord:
    def __init__(self, typeID, quantity, cost):
        self.typeID = typeID
        self.quantity = quantity
        self.cost = cost

    def __str__(self):
        return f"{self.typeID} {self.quantity} {self.cost}"

    def __repr__(self):
        return f"{self.typeID} {self.quantity} {self.cost}"
    
class BPCRecord:
    def __init__(self, typeID, me, te, cost):
        self.typeID = typeID
        self.me = me
        self.te = te
        self.cost = cost

    def __str__(self):
        return f"{self.typeID} {self.me} {self.te} {self.cost}"

    def __repr__(self):
        return f"{self.typeID} {self.me} {self.te} {self.cost}"