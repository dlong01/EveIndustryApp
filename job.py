import sqlite3
from activity import Activity
from textOuput import Formatter
import utils

class Job:
    def __init__(self, product, activity_id, runs):
        self.activity = Activity(product, activity_id, runs)

    def display_simple(self):
        with Formatter() as formatter:
            self.activity.display_simple_recipie(formatter)

    def display_complete(self):
        with Formatter() as formatter:
            self.activity.display_complete_recipie(formatter)

    def create_shopping_list(self):
        resources = self.activity.get_raw_resources()
        with Formatter() as formatter:
            with open("shopping_list.csv", "w") as shopping_list:
                print("Shopping List:")
                formatter.increase_indent()
                for resource in resources:
                    formatter.print(f"{resource.to_get}x {resource.type_name}")
                    shopping_list.write(f"{resource.type_name}\t{resource.to_get}\n")

    def calculate_item_sources(self):
        for ingredient in self.activity.ingredients:
            if ingredient.activity:
                ingredient.activity.ingredient
        return   True

    def get_item_stock(self, type_id):
        conn = sqlite3.connect(utils.WAREHOUSE_DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT quantity FROM warehouse WHERE item = ?", (type_id,))
        quantity = cursor.fetchone()
        conn.close()
        if quantity:
            return quantity[0]

    def calculate_cost(self):
        total_cost = 0
        for ingredient in self.activity.ingredients:
            total_cost += ingredient.calculate_cost()
        return total_cost