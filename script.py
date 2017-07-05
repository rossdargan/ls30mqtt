#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import os
import datetime
import subprocess

#Read Password

mqttHost = os.environ.get('MQTT_HOST')

print ("Host: " + mqttHost)

password = None
passwordLocation = os.environ.get('MQTT_PASSWORD_LOCATION', None)

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
  if rc==0:
     print("Connected with result code "+str(rc))
     client.subscribe("alarm/mode")
  else:
     print("Error connecting - got result code: " + str(rc))
     client.disconnect()


def on_message(client, userdata, msg):
  mode = msg.payload.decode()
  print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "   Recieved Request: " + mode)

  var = "/var/LS30/"
  pipe = subprocess.Popen(["perl", "/var/LS30/bin/arm.pl","-m", mode], stdin=subprocess.PIPE)

  client.publish("alarm/events/Remote Control/System", mode + " Mode");

client = mqtt.Client()

if passwordLocation != None:
   print("Checking for password from secret")
   passFile = open("/run/secrets/"+passwordLocation, "r")
   password = passFile.readline().rstrip()
   username = os.environ.get('MQTT_USERNAME')
   print ("Password Found:" + password)
   print ("Username: " + username)
   client.username_pw_set(username, password)

client.on_connect = on_connect
client.on_message = on_message
print ("Connecting...")
client.connect(mqttHost,1883,60)
print ("Connected")

client.loop_forever()
