import sqlite3
import utils

class Ingredient:
    def __init__(self, type_id, quantity, activity):
        self.type_id = type_id
        self.quantity = quantity
        self.activity = activity

        conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
        cursor = conn.cursor()

        # Getting the name of the product 
        cursor.execute("SELECT typeName FROM invTypes WHERE typeID = ?", (self.type_id,))
        self.type_name = cursor.fetchone()[0]

    def output_ingredient_simple(self, formatter):
        formatter.print(f"{self.type_name} x{self.quantity}")
    
    def output_recipie(self, formatter):
        if self.activity == None:
            self.output_ingredient_simple(formatter)
        else:
            self.activity.display_complete_recipie(formatter)
            