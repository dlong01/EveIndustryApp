import sqlite3
import utils
from ingredient import Ingredient
import math

class Activity:
    def __init__(self, product_id, activity_id, desired_quantity):
        self.activity_id = activity_id
        self.product_id = product_id
        self.ingredients = []
        self.desired_quantity = desired_quantity

        # Temporary step to input efficiency
        # TODO: calculate efficiency automatically with stored BPC efficiency
        type_name = self.get_product_name()

        if type_name:
            me = -1
            while me < 0 or me > 10:
                me = int(input(f"Enter the ME for {type_name}: "))
            self.matt_eff = utils.calculate_matt_efficiency(int(me)/100)

        conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
        cursor = conn.cursor()

        # Getting the activity's typeID and output quantity 
        cursor.execute("SELECT typeID, quantity FROM industryActivityProducts WHERE productTypeID = ? AND activityID = ?", (self.product_id, self.activity_id))
        activity_info = cursor.fetchone()

        if activity_info:
            self.type_id = activity_info[0]
            self.quantity = activity_info[1]
            self.runs = math.ceil(desired_quantity / self.quantity)

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
            material_quantity = math.ceil((material[1] * self.runs) * self.matt_eff)

            if material_quantity < self.runs:
                material_quantity = self.runs

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
    
    def display_simple_recipie(self, formatter):
        formatter.print(f"{self.get_product_name()} x{self.desired_quantity}")
        formatter.increase_indent()
        for ingredient in self.ingredients:
            ingredient.output_ingredient_simple(formatter)
            
        formatter.decrease_indent()

    def display_complete_recipie(self, formatter):
        formatter.print(f"{self.get_product_name()} x{self.desired_quantity}")
        formatter.increase_indent()
        for ingredient in self.ingredients:
            ingredient.output_recipie(formatter)

        formatter.decrease_indent()