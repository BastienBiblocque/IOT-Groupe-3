import paho.mqtt.client as mqtt
import json
import time
import random

# Fichier utilisé pour tester le broken avec des données fictives

broker = "localhost"
port = 1883
topic_prefix = "zigbee2mqtt/test/"

# Fonction pour simuler la récupération de données de différentes sondes
def get_sensor_data(sensor_id):
    temperature = round(random.uniform(20.0, 30.0), 2)  # Simuler une température
    return {
        "sensor_id": sensor_id,
        "temperature": temperature
    }

# Fonction de rappel pour la connexion
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print("Connect failed with code", rc)

client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker, port, 60)
client.loop_start()  # Démarrer la boucle pour gérer la connexion

try:
    while True:
        # Simuler l'envoi des données de 3 sondes
        for sensor_id in range(1, 3):
            data = get_sensor_data(f"sensor_{sensor_id}")
            topic = topic_prefix + data["sensor_id"]
            message = json.dumps(data)
            client.publish(topic, message)
            print(f"Published: {message} to topic: {topic}")

        # Pause de 30 secondes entre chaque envoi
        time.sleep(30)

except KeyboardInterrupt:
    print("Stopping publisher...")

finally:
    client.loop_stop()
    client.disconnect()
