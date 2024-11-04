import mysql.connector
from mysql.connector import errorcode

DATABASE_NAME = "AreaAvailabilityAnalyser"
TABLE_HEADER = "AreaAvailability (`Date`, `Usage`, `Availability`)"
DUPLICATE_CLAUSE = F"ON DUPLICATE KEY UPDATE `Usage` = VALUES(`Usage`), `Availability` = VALUES(`Availability`);"

def connect_to_main():
    try:
        cnx = mysql.connector.connect(user='root', password='Panoramic56',host='127.0.0.1')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx

def add_row(connection: mysql.connector.connection_cext.CMySQLConnection, datetime: str, usage:int, availability:int):
    try:
        cursor = connection.cursor()
        
        cursor.execute(f"USE {DATABASE_NAME}")
        connection.commit()
        
        query = f"INSERT INTO {TABLE_HEADER} VALUES ('{datetime}', {usage}, {availability}) {DUPLICATE_CLAUSE}"
        
        cursor.execute(query)
        connection.commit()
        
    except Exception as e:
        print(e)
        
def get_all(connection: mysql.connector.connection_cext.CMySQLConnection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"USE {DATABASE_NAME}")
        connection.commit()
        
        cursor.execute("SELECT * FROM AreaAvailability")
        return cursor.fetchall()
        
    except Exception as e:
        print(e)
        
def close_connection(connection: mysql.connector.connection_cext.CMySQLConnection):
    connection.close()    