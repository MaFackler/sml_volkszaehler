from paho.mqtt import client as mqtt


class Sender:

    def __init__(self, data):
        self._data = data

    def on_connect(self, client, userdata, flags, reason_code, porperties):
        for obis, value in self._data.items():
            client.publish(f"SML/{obis}", str(value))


def run(broker: str, data: dict):
    sender = Sender(data)
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = sender.on_connect

    client.connect(broker, 1883)
    client.loop_start()
    client.loop_stop()
