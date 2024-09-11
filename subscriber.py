import paho.mqtt.client as mqtt
import json
import requests
import threading
from datetime import datetime
import time
from collections import defaultdict, deque

broker = "localhost"
port = 1883
# topic_prefix = "sensors/temperature/#"  # Abonnement à tous les topics des sondes fictives
topic_prefix = "zigbee2mqtt/#"
HTTP_ENDPOINT = "http://localhost:5000/api/temperature"  # URL du backend

# Buffer pour stocker les données des sondes
sensor_data = defaultdict(list)

data_queue = deque()

# Verrou pour protéger l'accès au buffer
data_lock = threading.Lock()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(topic_prefix)
    else:
        print("Connect failed with code", rc)

# Fonction callback pour la réception des messages MQTT
def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        sensor_id = msg.topic.split('/')[-1]
        temperature = data.get("temperature")

        if temperature is not None:
            with data_lock:
                # Ajouter la température au buffer pour le périphérique correspondant
                sensor_data[sensor_id].append({
                    "temperature": temperature,
                    "timestamp": time.time()  # Utiliser le timestamp Unix pour chaque mesure
                })
            print(f"Received data: {data} from topic: {msg.topic}")
        else:
            print(f"Invalid message format or no temperature data: {data}")

    except json.JSONDecodeError:
        print(f"Failed to decode message: {msg.payload.decode()}")

# Fonction pour envoyer les données agrégées toutes les minutes via HTTP POST
def send_aggregated_data():
    while True:
        time.sleep(60)  # Attendre 1 minute
        with data_lock:
            if sensor_data:
                aggregated_data = []
                for sensor_id, readings in sensor_data.items():
                    for reading in readings:
                        aggregated_data.append({
                            "sonde_id": sensor_id,
                            "temperature":reading["temperature"],
                            "timestamp":reading["timestamp"]
                        })

                # Ajouter les données à la file d'attente
                data_queue.append(aggregated_data)

                # Vider le buffer après ajout à la file d'attente
                sensor_data.clear()

                while data_queue:
                    data_to_send = data_queue.popleft()

                try:
                    # Envoyer les données agrégées au backend via une requête POST
                    response = requests.post(HTTP_ENDPOINT, json=data_to_send)
                    response.raise_for_status()  # Vérifie si la requête a échoué
                    print(f"Data sent successfully to backend: {aggregated_data}")
                except requests.exceptions.RequestException as e:
                    print(f"Failed to send data: {e}")
                    # En cas d'échec, ré-ajouter les données à la fin de la file d'attente pour réessayer plus tard
                    data_queue.append(data_to_send)
                    break  # Sortir de la boucle pour essayer à nouveau plus tard

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, 60)

# Lancer le thread qui envoie les données agrégées toutes les minutes via HTTP
aggregator_thread = threading.Thread(target=send_aggregated_data)
aggregator_thread.daemon = True  # Pour que le thread se termine quand le programme se termine
aggregator_thread.start()

client.loop_forever()
