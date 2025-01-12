from activity import Activity
from textOuput import Formatter

class Job:
    def __init__(self, product, activity_id, runs):
        self.activity = Activity(product, activity_id, runs)

    def display_simple(self):
        with Formatter() as formatter:
            self.activity.display_simple_recipie(formatter)

    def display_complete(self):
        with Formatter() as formatter:
            self.activity.display_complete_recipie(formatter)

    def display_shopping_list(self):
        resources = self.activity.get_raw_resources()
        with Formatter() as formatter:
            with open("shopping_list.csv", "a") as shopping_list:
                print("Shopping List:")
                formatter.increase_indent()
                for resource in resources:
                    formatter.print(f"{resource.type_name}\t{resource.quantity}")
                    shopping_list.write(f"{resource.type_name}\t{resource.quantity}\n")