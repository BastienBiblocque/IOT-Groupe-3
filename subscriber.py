import paho.mqtt.subscribe as subscribe

print("start")

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    userdata["message_count"] += 1
    # if userdata["message_count"] >= 5:
        # it's possible to stop the program by disconnecting
        # client.disconnect()

subscribe.callback(on_message_print, "zigbee2mqtt/0xf0f5bdfffe2d1ea8", hostname="mqtt", userdata={"message_count": 0})