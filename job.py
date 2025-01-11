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

    def display_raw_resources(self):
        resources = self.activity.get_raw_resources()
        with Formatter() as formatter:
            for resource in resources:
                resource.output_ingredient_simple(formatter)