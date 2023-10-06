from paho.mqtt import client as mqtt

def on_connect(client: mqtt.Client, userdata, flags, rc):
    if rc == 0:
        print('Connected to MQTT broker')
    else:
        print("Bad connection to MQTT broker, returned code=", rc)

def on_publish(client, userdata, mid):
    print('Published')

def get_mqtt_client() -> mqtt.Client:
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    return client