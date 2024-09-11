# IOT-Groupe-3

## Version local

- Installer Moquitto https://mosquitto.org/download/
- Lancer Mosquitto `mosquitto -v`
- Lancer Publisher `python3 publisher.py` (Pour tester le fonctionnement du subscriber, en version finale, le publisher sera zeegbee2mqtt qui receptionnera les données des sondes)
- Lancer Subscriber `python3 subscriber.py` (En version test avec le publisher: topic_prefix = "sensors/temperature/#"; en version finale avec la sonde: topic_prefix = "zigbee2mqtt/#")

#### Pour tester la solution sans sonde et sans backend receveur:

- Dans le Publisher, les lignes suivantes génèrent des données fictives de sondes (toutes les 10 secondes actuellement):
  `for sensor_id in range(1, 4):
data = get_sensor_data(f"sensor*{sensor_id}")
topic = topic_prefix + data["sensor_id"]
message = json.dumps(data)
client.publish(topic, message)
print(f"Published: {message} to topic: {topic}")
time.sleep(10)`

- Pour utiliser le backend, installer flask (`pip install flask`)
- Un backend de test peut être démarré pour vérifier l'envoi des données:
  `python3 backend_for_test.py`

### Version Shell :

- Lancer Publisher `mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"`
- Lancer Subcscriber `mosquitto_sub -h localhost -t test/topic`
- Dans tout les cas on a besoin de Mosquitto et de `mosquitto -v`

### Version local avec Python :

- Installer `paho.mqtt.client`
- Le fichier publisher remplace la fonction publisher, de même pour la version subscriber
- Dans tout les cas on a besoin de Mosquitto et de `mosquitto -v`
