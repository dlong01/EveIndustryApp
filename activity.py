import sqlite3
import utils
from ingredient import Ingredient
import math

class Activity:
    def __init__(self, product_id, activity_id, required):
        self.activity_id = activity_id
        self.product_id = product_id
        self.ingredients = []
        self.required_quantity = required

        conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
        cursor = conn.cursor()

        # Getting the activity's typeID and output quantity 
        cursor.execute("SELECT typeID, quantity FROM industryActivityProducts WHERE productTypeID = ? AND activityID = ?", (self.product_id, self.activity_id))
        activity_info = cursor.fetchone()

        if activity_info:
            self.type_id = activity_info[0]
            self.produced = activity_info[1]
            self.runs = math.ceil(required / self.produced)

            cursor.execute("SELECT materialTypeID, quantity FROM industryActivityMaterials WHERE  typeID = ? AND activityID = ?", (self.type_id, self.activity_id))
            materials = cursor.fetchall()

            self.handle_ingredients(materials)
        else:
            return None

        conn.close()

    def handle_ingredients(self, materials):  
        conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
        cursor = conn.cursor()

        # Creating ingredient to produce required material
        for material in materials:
            cursor.execute("SELECT 1 FROM industryActivityProducts WHERE productTypeID = ? AND activityID = ?", (material[0], self.activity_id))
            material_quantity = math.ceil(material[1] * self.runs)

            if cursor.fetchone():
                prod_activity = Activity(material[0], self.activity_id, material_quantity)
                self.ingredients.append(Ingredient(material[0], material_quantity, prod_activity))
            else:
                self.ingredients.append(Ingredient(material[0], material_quantity, None))

    def get_product_name(self):
        conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
        cursor = conn.cursor()

        # Getting the name of the product 
        cursor.execute("SELECT typeName FROM invTypes WHERE typeID = ?", (self.product_id,))
        product_name = cursor.fetchone()[0]

        conn.close()
        return product_name

    def get_raw_resources(self):
        raw_resources = []
        for ingredient in self.ingredients:
            if ingredient.activity is None:
                raw_resources.append(ingredient)
            else:
                for item in ingredient.activity.get_raw_resources():
                    present = False
                    for resource in raw_resources:
                        if item.type_id == resource.type_id:
                            resource.quantity += item.quantity
                            present = True
                            break
                    if not present:
                        raw_resources.append(item)

        return raw_resources
    
    def get_ingredients(self):
        return self.ingredients
    
    def display_simple_recipie(self, formatter):
        formatter.print(f"{self.get_product_name()} x{self.required_quantity}")
        formatter.increase_indent()
        for ingredient in self.ingredients:
            ingredient.output_ingredient_simple(formatter)
            
        formatter.decrease_indent()

    def display_complete_recipie(self, formatter):
        formatter.print(f"{self.get_product_name()} x{self.required_quantity}")
        formatter.increase_indent()
        for ingredient in self.ingredients:
            ingredient.output_recipie(formatter)

        formatter.decrease_indent()