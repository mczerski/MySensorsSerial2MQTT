import paho.mqtt.client as mqtt
import serial
import time
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--broker-host', default='localhost')
parser.add_argument('--broker-port', type=int, default=1883)
parser.add_argument('--device', required=True)
args = parser.parse_args()

rootTopic = 'mySensors'

client = mqtt.Client()
client.connect(args.broker_host, args.broker_port)
client.subscribe(rootTopic + "in/#")

ser = serial.Serial(args.device, 115200, timeout=1)

def mqtt_on_message(client, obj, msg):
    print 'received topic: %s. payload: %s' % (msg.topic, msg.payload)
    fields = msg.topic.split('/')
    data = ";".join(fields[1:] + [msg.payload]).encode()
    print 'writing msg: %s' % data
    ser.write(data + '\n')

client.on_message = mqtt_on_message
client.loop_start()

run =[True]

def read_from_port():
    while run[0]:
        reading = ser.readline().decode().strip()
        if not reading:
            continue
        print reading.strip()
        fields = reading.split(';')
        if len(fields) != 6:
            continue
        print 'received msg: %s' % reading
        topic = "/".join([rootTopic+'out'] + fields[:-1])
        print 'sending topic: %s. payload: %s' % (topic, fields[-1])
        client.publish(topic, fields[-1])

thread = threading.Thread(target=read_from_port)
thread.start()

try:
    while True:
        time.sleep(100)
except:
    run[0] = False
    client.loop_stop()
