import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time
import mysql.connector


print("toto")

broker = "mqtt"
port = 1883
# topic_prefix = "sensors/temperature/#"  # Abonnement à tous les topics des sondes fictives
topic_prefix = "zigbee2mqtt/#"

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

# Fonction pour insérer des données dans la base
def insert_sensor_data(sensor_id, temperature, timestamp):
    db = connect_db()
    cursor = db.cursor()

    insert_query = """
    INSERT INTO sensor_data (sensor_id, temperature, measure_timestamp)
    VALUES (%s, %s, FROM_UNIXTIME(%s))
    """
    cursor.execute(insert_query, (sensor_id, temperature, timestamp))
    db.commit()
    cursor.close()
    db.close()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(topic_prefix)
    else:
        print("Connect failed with code", rc)

# Fonction callback pour la réception des messages MQTT
def on_message(client, userdata, msg):
    try:
        print('message:')
        # data = json.loads(msg.payload)
        # if "temperature" in data:
        #     print(data)
        # else:
        #     print('other')
        #     print(type(data))
        # sensor_id = msg.topic.split('/')[-1]
        # temperature = data.get("temperature")

        # if temperature is not None:
        #     timestamp = int(time.time())

        #     # Enregistrer dans la base de données
        #     insert_sensor_data(sensor_id, temperature, timestamp)

        #     print(f"Received data: {data} from topic: {msg.topic}")
        # else:
        #     print(f"Invalid message format or no temperature data: {data}")

    except json.JSONDecodeError:
        print(f"Failed to decode message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)
client.loop_forever()
