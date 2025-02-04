import sqlite3
import facility_details
import manufacture
import utils
import warehousing

def main():
    print("Welcome to Eve Industry App!")

    print("Checking databases...")

    if not check_eve_db():
        print("FATAL - db not found")

    warehousing.verify_warehouse()

    while(True):
        print("\nOptions:")
        print("\t1 - View a recipie")
        print("\t2 - Manufacture a product")
        print("\t3 - Update the warehouse")
        print("\t4 - Input tax rates")

        print("\t0 - Exit")
        option = input("Enter the option: ")
        if option == "1":
            manufacture.view_recipie()
        elif option == "2":
            manufacture.create_job()
        elif option == "3":
            warehousing.update_warehouse()
        elif option == "4":
            facility_details.update_facility_details()
        elif option == "0":
            break
        else:
            print("Invalid option")
        
def check_eve_db():
    conn = sqlite3.connect(utils.EVE_DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type LIKE 'table';")
    tables = cursor.fetchall()

    if len(tables) == 0:
        print("Database not found")
        return False
    else:
        print("Database found")
        return True

if __name__ == "__main__":
    main()