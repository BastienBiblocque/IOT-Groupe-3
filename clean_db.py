import mysql.connector
from datetime import datetime

# Connexion à la base de données MySQL
db_config = {
    'user': 'iot',
    'password': 'iot',
    'host': 'mysql',
    'port': 3306,
    'database': 'temperatures_data',
}

def connect_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def delete_old_data():
    try:
        conn = connect_db()
        if conn is None:
            return
        
        cursor = conn.cursor()

        delete_query = """
        DELETE FROM sensor_data
        WHERE sending_timestamp < NOW() - INTERVAL 7 DAY
        """
        cursor.execute(delete_query)

        conn.commit()

        print(f"Deleted {cursor.rowcount} rows from sensor_data")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    delete_old_data()
