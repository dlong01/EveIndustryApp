import sqlite3
from job import Job
import utils

MANUFACTURING_PROCESS_ID = 1

def init_job():

    # Connect to the EVE database
    conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
    cursor = conn.cursor()

    product = input("\nEnter the product to manufacture: ")

    # Getting the typeID of the product
    cursor.execute("SELECT typeID FROM invTypes WHERE typeName = ? COLLATE NOCASE", (product,))
    product_id = cursor.fetchone()

    if product_id:
        product_id = product_id[0]
    else:
        print("Product not found")
        return -1

    conn.close()

    if not(product_id):
        return -1
    else:
        runs = int(input("Enter the number of runs: "))
        job = Job(product_id, MANUFACTURING_PROCESS_ID, runs)

    if job:
        option = input("What information would you like to see? (1) Full Job, (2) Materials Shopping list, (3) Job time: ")

        if option == "1":
            job.display_complete()
        elif option == "2":
            job.display_shopping_list()
        elif option == "3":
            print("not implemented")
    else:
        print("Unable to create job")
        return -1
