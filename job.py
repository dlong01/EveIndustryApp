import math
import os
import sqlite3
from activity import Activity
import api_requests
import facility_details
from ingredient import Ingredient
from textOuput import Formatter
import utils

class Job:
    def __init__(self, product, activity_id, needed_quantity):
        self.activity = Activity(product, activity_id, needed_quantity)
        self.runs = self.activity.runs
        self.product_name = product
        self.needed_quantity = needed_quantity
        self.bp_me = 1-(float(input("Enter the ME level of the blueprint: "))/100)
        self.calculate_material_list(facility_details.get_me_modifier(self.get_group_id()))
        self.calculate_estimated_cost()
        self.estimated_income = needed_quantity * api_requests.get_average_market_price(self.activity.product_id)
        self.income_post_sales_tax = self.estimated_income * (1+0.0203) * (1+0.01)
        print(f"Estimated profit: {round(self.estimated_income - self.estimated_cost,2)} ISK \tMargin: {round(100*((self.estimated_income/self.estimated_cost)-1), 2)}%")

    def display_simple(self):
        with Formatter() as formatter:
            self.activity.display_simple_recipie(formatter)

    def display_complete(self):
        with Formatter() as formatter:
            self.activity.display_complete_recipie(formatter)

    def create_todo_lists(self):
        job_folder_path = f"jobs/{self.needed_quantity}x{self.activity.get_product_name()}"
        os.makedirs(job_folder_path, exist_ok=True)

        shopping_list = "Buy:\n"
        production_list = "Build:\n"
        for ingredient in self.ingredients:
            if ingredient.activity is None:
                to_buy = ingredient.quantity - self.get_item_stock(ingredient.type_id) 
                if to_buy > 0:
                    shopping_list += f"{to_buy} {ingredient.type_name}\n"
            else:
                to_build = ingredient.quantity - self.get_item_stock(ingredient.type_id)
                if to_build > 0:
                    production_list += f"{to_build} {ingredient.type_name}\n"

        with open(f"{job_folder_path}/shopping_list.txt", "w") as shopping_list_file:
            shopping_list_file.write(shopping_list)
        
        with open(f"{job_folder_path}/production_list.txt", "w") as production_list_file:
            production_list_file.write(production_list)

    def calculate_material_list(self, me_bonus):
        activity_ingredients = self.activity.get_ingredients()
        self.ingredients = []
        for a_ingredient in activity_ingredients:
            needed_quantity = math.ceil(a_ingredient.quantity * self.bp_me * me_bonus)
            if needed_quantity < self.runs:
                needed_quantity = self.runs
            self.ingredients.append(Ingredient(a_ingredient.type_id, needed_quantity, a_ingredient.activity))

    def get_item_stock(self, type_id):
        conn = sqlite3.connect(utils.WAREHOUSE_DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT quantity FROM items WHERE typeID LIKE ?", (type_id,))
        quantity = cursor.fetchone()
        conn.close()
        if quantity:
            return quantity[0]
        else:
            return 0

    def calculate_estimated_cost(self):
        self.estimated_cost = 0
        system_id, job_cost_modifier, tax_rate = facility_details.get_install_modifiers()

        self.estimated_cost += self.calculate_install_cost(system_id, job_cost_modifier, tax_rate)
        self.estimated_cost += self.calculate_material_cost()
        
    def calculate_install_cost(self, system_id, job_cost_modifier, tax_rate):
        eiv = self.calculate_eiv()
        
        system_cost_index = api_requests.get_system_cost_index(system_id)
        gross_cost = eiv * ((system_cost_index * (100-job_cost_modifier))/100)
        tax_cost = eiv * ((tax_rate)/100)
        install_cost = gross_cost + tax_cost
        return install_cost
    
    def calculate_material_cost(self):
        material_cost = 0
        conn = sqlite3.connect(utils.WAREHOUSE_DATABASE_PATH)
        cursor = conn.cursor()
        for ingredient in self.ingredients:
            cursor.execute("SELECT cost FROM items WHERE typeID LIKE ?", (ingredient.type_id,))
            cost = cursor.fetchone()

            if cost:
                material_cost += ingredient.quantity * cost[0]
            else:
                material_cost += ingredient.quantity * api_requests.get_average_market_price(ingredient.type_id)
        return material_cost

    def calculate_eiv(self):
        eiv = 0
        for ingredient in self.activity.ingredients:
            eiv += ingredient.quantity * api_requests.get_adjusted_market_price(ingredient.type_id)
        return eiv
    
    def get_group_id(self):
        conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT groupID FROM invTypes WHERE typeID LIKE ?", (self.activity.product_id,))
        group_id = cursor.fetchone()[0]
        conn.close()
        return group_id