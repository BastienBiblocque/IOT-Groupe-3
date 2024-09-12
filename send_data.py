import requests
import mysql.connector
from datetime import datetime

HTTP_ENDPOINT = "http://host.docker.internal:5000/api/temperature"


# Connexion à la base de données MySQL
db_config = {
    'user': 'iot',
    'password': 'iot',
    'host': 'mysql',
    'port':3306,
    'database': 'temperatures_data',
}

def connect_db():
    return mysql.connector.connect(**db_config)

def fetch_data_to_send():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    
    # Sélectionner les données à envoyer (sans sending_timestamp)
    select_query = """
    SELECT sensor_id, temperature, measure_timestamp
    FROM sensor_data
    WHERE sending_timestamp IS NULL
    """
    cursor.execute(select_query)
    rows = cursor.fetchall()
    
    # Grouper les données par passerelle
    data = {
        "passerellePhysicalId": "passerelle_1",
        "sondeTemperatureDtoList": []
    }
    
    for row in rows:
        data["sondeTemperatureDtoList"].append({
            "sonde_id": row["sensor_id"],
            "temperature": row["temperature"],
            "timestamp": int(row["measure_timestamp"].timestamp())  # Convertir en timestamp Unix
        })
    
    cursor.close()
    db.close()
    
    return data

def update_sent_data(sensor_ids):
    db = connect_db()
    cursor = db.cursor()
    
    # Mettre à jour le champ sending_timestamp pour les données envoyées
    update_query = """
    UPDATE sensor_data
    SET sending_timestamp = NOW()
    WHERE sensor_id IN (%s)
    """
    
    format_strings = ','.join(['%s'] * len(sensor_ids))
    cursor.execute(update_query % format_strings, tuple(sensor_ids))
    
    db.commit()
    cursor.close()
    db.close()

def send_data():
    data_to_send = fetch_data_to_send()

    print(data_to_send)
    
    if not data_to_send["sondeTemperatureDtoList"]:
        print("No data to send.")
        return

    try:
        response = requests.post(HTTP_ENDPOINT, json=data_to_send)
        response.raise_for_status()  # Vérifie si la requête a échoué
        print("Data sent successfully.")
        
        # Mettre à jour la base de données après envoi réussi
        sensor_ids = [item["sonde_id"] for item in data_to_send["sondeTemperatureDtoList"]]
        update_sent_data(sensor_ids)
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data: {e}")

if __name__ == "__main__":
    send_data()
