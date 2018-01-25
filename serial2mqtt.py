#!/usr/bin/python3

import paho.mqtt.client as mqtt
import serial
from serial.threaded import ReaderThread, LineReader
import time
import argparse

class MySerialReader(LineReader):
    TERMINATOR = b'\n'
    I_LOG_MESSAGE = '9'

    def __init__(self, rootTopic, mqttClient):
        super(MySerialReader, self).__init__()
        self._rootTopic = rootTopic
        self._mqttClient = mqttClient

    def handle_line(self, line):
        print(line)
        fields = line.split(';')
        if len(fields) != 6:
            return
        if fields[4] == self.I_LOG_MESSAGE:
            return
        topic = "/".join([self._rootTopic+'out'] + fields[:-1])
        print('sending topic: %s. payload: %s' % (topic, fields[-1]))
        self._mqttClient.publish(topic, fields[-1])

class Serial2MQTT:
    def __init__(self, device, host, port, rootTopic):
        self._rootTopic = rootTopic
        self._mqttClient = mqtt.Client()
        self._mqttClient.connect(host, port)
        self._mqttClient.subscribe(self._rootTopic + "in/#")
        self._mqttClient.on_message = self._mqtt_on_message
        ser = serial.Serial(args.device, 115200, timeout=1)
        self._serialClient = ReaderThread(ser, lambda: MySerialReader(self._rootTopic, self._mqttClient))
        self._serialProtocol = None

    def _mqtt_on_message(self, client, obj, msg):
        payload = msg.payload.decode("utf-8")
        print ('received topic: %s. payload: %s' % (msg.topic, payload))
        fields = msg.topic.split('/')
        data = ";".join(fields[1:] + [payload])
        print ('writing msg: %s' % data)
        self._serialProtocol.write_line(data)

    def run(self):
        self._serialClient.start()
        _, self._serialProtocol = self._serialClient.connect()
        self._mqttClient.loop_start()

    def stop(self):
        self._mqttClient.loop_stop()
        self._serialClient.stop()

parser = argparse.ArgumentParser()
parser.add_argument('--broker-host', default='localhost')
parser.add_argument('--broker-port', type=int, default=1883)
parser.add_argument('--device', required=True)
args = parser.parse_args()

rootTopic = 'mySensors'

serial2Mqtt = Serial2MQTT(args.device, args.broker_host, args.broker_port, rootTopic)
serial2Mqtt.run()

try:
    while True:
        time.sleep(100)
except:
    serial2Mqtt.stop()

