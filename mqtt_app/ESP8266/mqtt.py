from umqtt.simple import MQTTClient
import ubinascii
import ujson
from machine import unique_id
import sys

MQTT_SERVER = '192.168.178.66'
MQTT_USER = 'volker'
MQTT_PASSWORD = 'xxx'

UID = ubinascii.hexlify(unique_id())
TOPIC = 'tinkershop/eink'


class MQTT(object):
    def __init__(self, logger=None):
        if not logger:
            self.logger = print
        else: 
            self.logger = logger
            
        self.client = None
        self.logger('connecting to MQTT_Client {}'.format(MQTT_SERVER))
        try:
            self.client = MQTTClient(UID, MQTT_SERVER, user=MQTT_USER, password=MQTT_PASSWORD)
            self.client.set_callback(self.callback)
            self.client.connect()
    
        except Exception as e:
            sys.print_exception(e)
            self.logger('No Connection to MQTT broker {}'.format(MQTT_SERVER))
            self.client = None
            return        
        self.logger('Connected to MQTT broker {}'.format(MQTT_SERVER))

    def publish(self, data, topic=TOPIC):
        if self.client is None:
            return
        
        json = ujson.dumps({UID:data})
        self.client.publish(topic, json)

    def callback(self):
        self.logger('callback')
        
    def disconnect(self):
        self.client.disconnect()
