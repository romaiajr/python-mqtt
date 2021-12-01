import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = 'my secret key'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'maqiatto.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'romaiajr5@gmail.com'
app.config['MQTT_PASSWORD'] = '7711'
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    mqtt.publish("romaiajr5@gmail.com/web","teste")
    return "funcionou"


@socketio.on('publish')
def handle_publish():
    mqtt.publish("romaiajr5@gmail.com/web","teste")
    return True

@socketio.on('subscribe')
def handle_subscribe():
    mqtt.subscribe("romaiajr5@gmail.com/web")


@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    mqtt.unsubscribe_all()


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    handle_event(data['payload'])
    socketio.emit('mqtt_message', data=data)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

def handle_event(payload):
    msg = payload.split(',')
    event = msg[0]
    device_id = msg[1]

if __name__ == '__main__':
    # handle_subscribe()
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)