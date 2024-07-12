# IOT-Groupe-3

## Version local

- Installer Moquitto https://mosquitto.org/download/
- Lancer Mosquitto ``mosquitto -v``

### Version Shell :
- Lancer Publisher ``mosquitto_pub -h localhost -t test/topic -m "Hello MQTT"``
- Lancer Subcscriber ``mosquitto_sub -h localhost -t test/topic``
- Dans tout les cas on a besoin de Mosquitto et de `mosquitto -v`

### Version local avec Python : 

- Installer ``paho.mqtt.client``
- Le fichier publisher remplace la fonction publisher, de même pour la veersion subscriber
- Dans tout les cas on a besoin de Mosquitto et de `mosquitto -v`