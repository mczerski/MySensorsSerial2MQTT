# MySensorsSerial2MQTT
This is simple bridge between MySensors serial gateway and the MQTT bus.

To use it, connect the serial gateway to the host and then run:
./serial2mqtt.py --device /dev/ttyDevice
where /dev/ttyDevice is the path to the serial device (e.g. /dev/ttyACM0 for Arduino Uno serial gateway).

To run it as a system service You can use mySerial2mqtt.service.
