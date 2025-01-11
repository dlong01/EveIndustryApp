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
        job.display_simple()
        print("\n")
        job.display_complete()
        print("\n")
        job.display_raw_resources()
    else:
        print("Unable to create job")
        return -1
