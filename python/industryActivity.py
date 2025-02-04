import sqlite3

EVE_DB_PATH = './data/eve.db'

class industryActivity:
    def __init__(self, typeID, activtiyID):
        try:
            self.typeID, self.activityID = self.__validateActivity(typeID, activtiyID)
        except ValueError as e:
            print(e.args[0])

    def __validateActivity(typeID, activityID):
        conn = sqlite3.connect(EVE_DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT time FROM industryActivity WHERE typeID = ? AND activityID = ?", (typeID, activityID))
        time = cursor.fetchone()

        if not time:
            raise ValueError(f"No activity for typeID: {typeID} and activityID: {activityID}")
        
        return typeID, activityID
    
    def loadMaterials()