import paho.mqtt.client as mqtt
import time
import mysql.connector
import json

topic='zigbee2mqtt/#'
def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        print(f"Broker rejected you subscription: {reason_code_list[0]}")
    else:
        print(f"Broker granted the following QoS: {reason_code_list[0].value}")

def on_unsubscribe(client, userdata, mid, reason_code_list, properties):
    # Be careful, the reason_code_list is only present in MQTTv5.
    # In MQTTv3 it will always be empty
    if len(reason_code_list) == 0 or not reason_code_list[0].is_failure:
        print("unsubscribe succeeded (if SUBACK is received in MQTTv3 it success)")
    else:
        print(f"Broker replied with failure: {reason_code_list[0]}")
    client.disconnect()

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

def on_message(client, userdata, message):
    data = json.loads(message.payload)

    if "temperature" in data:
        sensor_id = message.topic.split('/')[-1]
        insert_sensor_data(sensor_id, float(data.get("temperature")), int(time.time()))

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(topic)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

mqttc.user_data_set([])
mqttc.connect("mqtt")
mqttc.loop_forever()
# print(f"Received the following message: {mqttc.user_data_get()}")