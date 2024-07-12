import paho.mqtt.client as mqtt

broker = "localhost"
port = 1883
topic = "test/topic"
message = "Hello MQTT from Python on Windows!"

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
client.publish(topic, message)
print(f"Published: {message} to topic: {topic}")
client.loop_stop()  # Arrêter la boucle
client.disconnect()
