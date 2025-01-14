import math
import sqlite3
from activity import Activity
import api_requests
import facility_details
from ingredient import Ingredient
from textOuput import Formatter
import utils

class Job:
    def __init__(self, product, activity_id, runs):
        self.activity = Activity(product, activity_id, runs)
        self.runs = runs
        self.cost = self.calculate_estimated_cost()

    def display_simple(self):
        with Formatter() as formatter:
            self.activity.display_simple_recipie(formatter)

    def display_complete(self):
        with Formatter() as formatter:
            self.activity.display_complete_recipie(formatter)

    def create_shopping_list(self):
        print("Not implemented")
        # resources = self.activity.get_raw_resources()
        # with Formatter() as formatter:
            # with open("shopping_list.csv", "w") as shopping_list:
                # print("Shopping List:")
                # formatter.increase_indent()
                # for resource in resources:
                    # formatter.print(f"{resource.to_get}x {resource.type_name}")
                    # shopping_list.write(f"{resource.type_name}\t{resource.to_get}\n")

    def create_todo_list(self):
        self.calculate_material_list(facility_details.get_me_modifier(self.get_group_id()))
        to_do_list = ""
        for ingredient in self.ingredients:
            to_get = ingredient.quantity - self.get_item_stock(ingredient.type_id) 
            if to_get > 0:
                to_do_list += f"{to_get} {ingredient.type_name}\n"

        with open("todo_list.txt", "w") as todo_list:
            todo_list.write(to_do_list)

    def calculate_material_list(self, me_bonus):
        bp_me = int(input("Enter the ME level of the blueprint: "))
        activity_ingredients = self.activity.get_ingredients()
        self.ingredients = []
        print(f"me_bonus: {me_bonus} bp_me: {bp_me}")
        for a_ingredient in activity_ingredients:
            needed_quantity = math.ceil((self.runs * a_ingredient.quantity) * ((100 - (bp_me + me_bonus))/100))
            if needed_quantity < self.runs:
                needed_quantity = self.runs
            self.ingredients.append(Ingredient(a_ingredient.type_id, needed_quantity, a_ingredient.activity))

    def get_item_stock(self, type_id):
        conn = sqlite3.connect(utils.WAREHOUSE_DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT quantity FROM items WHERE typeID = ?", (type_id,))
        quantity = cursor.fetchone()
        conn.close()
        if quantity:
            return quantity[0]
        else:
            return 0

    def calculate_estimated_cost(self):
        cost = 0

        conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT groupID FROM invTypes WHERE typeID = ?", (self.activity.type_id,))
        group_id = cursor.fetchone()[0]

        system_id, job_cost_modifier, tax_rate = facility_details.get_install_modifiers()

        cost += self.calculate_install_cost(system_id, job_cost_modifier, tax_rate)
        #self.calculate_material_list(me_bonus)
        #self.get_material_cost()
        
    def calculate_install_cost(self, system_id, job_cost_modifier, tax_rate):
        eiv = self.calculate_eiv()
        
        system_cost_index = api_requests.get_system_cost_index(system_id)
        gross_cost = eiv * ((system_cost_index * (100-job_cost_modifier))/100)
        tax_cost = eiv * ((tax_rate)/100)
        print(f"{tax_rate}")
        install_cost = gross_cost + tax_cost
        print(f"{gross_cost}, {tax_cost}, {install_cost}")
        return install_cost

    def calculate_eiv(self):
        eiv = 0
        for ingredient in self.activity.ingredients:
            eiv += ingredient.quantity * api_requests.get_adjusted_market_price(ingredient.type_id)
        return eiv
    
    def get_group_id(self):
        conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT groupID FROM invTypes WHERE typeID = ?", (self.activity.type_id,))
        group_id = cursor.fetchone()[0]
        print(f"Group ID: {cursor.fetchall()}")
        conn.close()
        return group_id