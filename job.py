import sqlite3
from activity import Activity
import api_requests
from textOuput import Formatter
import utils

class Job:
    def __init__(self, product, activity_id, runs):
        self.activity = Activity(product, activity_id, runs)

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

    def get_item_stock(self, type_id):
        conn = sqlite3.connect(utils.WAREHOUSE_DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT quantity FROM warehouse WHERE item = ?", (type_id,))
        quantity = cursor.fetchone()
        conn.close()
        if quantity:
            return quantity[0]

    def calculate_estimated_cost(self):
        cost = 0

        cost += self.calculate_install_cost()
        #cost += self.calculate_material_cost()
        
    def calculate_install_cost(self):
        eiv = self.calculate_eiv()
        install_cost = eiv * 1
        # TODO : Add the cost of the job installation

        print(install_cost)
        return install_cost

    def calculate_eiv(self):
        eiv = 0
        for ingredient in self.activity.ingredients:
            eiv += ingredient.quantity * api_requests.get_adjusted_market_price(ingredient.type_id)
        return eiv