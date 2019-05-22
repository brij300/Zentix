#!/usr/bin/env python
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time, threading, ssl, random
import emailGenerator

# client, user and device details
serverUrl   = "iot.eclipse.org"
port        = 1883
device_name = "RPI_Room_1"
#clientId    = "000000003cb6b056"
#tenant      = ""
#username    = ""
#password    = ""
abc=0
abc_hum=0
listHumid=[]

receivedMessages = []

# display all incoming messages
def on_message(client, userdata, message):
    print("Received operation " + str(message.payload))
    if (message.payload.startswith("510")):
        print("Simulating device restart...")
        publish("s/us", "501,c8y_Restart")
        print("...restarting...")
        time.sleep(1)
        publish("s/us", "503,c8y_Restart")
        print("...done...")

# send temperature measurement
def sendMeasurements():
    try:
#        print("Sending temperature measurement...")
        abc = str(random.randint(22, 28))
        publish("sensor_data", abc)
        print(abc)
        thread = threading.Timer(7, sendMeasurements)
        thread.daemon=True
        thread.start()
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print('Received keyboard interrupt, quitting ...')

# send humidity measurement
def sendMeasurementsHumid():
    try:
#        print("Sending temperature measurement...")
        abc_hum = str(random.randint(45, 55))
        publish("sensor_data", abc_hum)
        print(abc_hum)
        alert_temp=int(abc_hum)
        #Appending all the values in the last for 5 min
        #listHumid.append(alert_temp) 
        #avg = sum(listHumid)/len(listHumid)
        # If average value for humidity sensor is > 80% for 5 min
        if(alert_temp>44):
            emailGenerator.send_message()
        thread = threading.Timer(7, sendMeasurementsHumid)
        thread.daemon=True
        thread.start()
        while True: time.sleep(100)
    except (KeyboardInterrupt, SystemExit):
        print('Received keyboard interrupt, quitting ...')


# publish a message
def publish(topic, message, waitForAck = False):
    mid = client.publish(topic, message, 2)[1]
    if (waitForAck):
        while mid not in receivedMessages:
            time.sleep(0.25)

def on_publish(client, userdata, mid):
    receivedMessages.append(mid)

# connect the client 
client= mqtt.Client()
client.on_message = on_message
client.on_publish = on_publish

client.connect(serverUrl, port,60)
client.loop_start()

print("Device registered successfully!")

client.subscribe("sensor_data")
sendMeasurements()
sendMeasurementsHumid()