import paho.mqtt.client as mqtt
import sys

BROKER_ADDRESS = "broker.emqx.io"
PORT = 1883
TOPIC = "/student_group/light_control"
CLIENT_ID = "python_iot_simulator"

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Connected to MQTT Broker!")
        client.subscribe(TOPIC)
        print(f"📡 Listening for messages on {TOPIC}")
    else:
        print(f"❌ Failed to connect, return code {rc}")
        sys.exit(1)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"📩 Message received: {message}")
    if message == "ON":
        print("💡 Light is TURNED ON")
    elif message == "OFF":
        print("💡 Light is TURNED OFF")
    else:
        print(f"⚠️ Unknown command: {message}")

client = mqtt.Client(client_id=CLIENT_ID, callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

print(f"🔄 Connecting to MQTT broker at {BROKER_ADDRESS}...")
try:
    client.connect(BROKER_ADDRESS, PORT, 60)
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

try:
    print("🚀 ESP8266 simulator started. Press Ctrl+C to exit.")
    client.loop_forever()
except KeyboardInterrupt:
    print("\n🛑 Simulator stopped by user")
    client.disconnect()
    sys.exit(0)
