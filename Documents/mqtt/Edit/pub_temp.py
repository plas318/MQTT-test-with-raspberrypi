import paho.mqtt.client as mqtt
import time
from datetime import datetime
from datetime import timedelta

import os
import re
import psutil
import mqconfig

MQ_HOST = mqconfig.mq_host
MQ_TITLE = mqconfig.mq_title

count = 0
def on_connect(client, userdata, flags, rc):
    print("Connect result: {}".format(mqtt.connack_string(rc)))
    client.connected_flag = True

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))

def on_message(client, userdata, msg):
    global count
    count +=1
    payload_string = msg.payload.decode('utf-8')
    print("{:d} Topic: {}. Payload: {}".format(count, msg.topic, payload_string))

def pubTempData(client, freq=10, limit=100):
    delta = 1/freq
    
    for i in range(limit*freq):
        ti = datetime.now()
        temp = os.popen("vcgencmd measure_temp").readline()
        da = re.findall(r'\d+\.\d+',temp.rstrip())[0]
        cpu_use = psutil.cpu_percent(interval=1)
        mem_tot = psutil.virtual_memory().total/(1024**2)#mb
        mem_use = psutil.virtual_memory().used/(1024**2)# mb
        #row = "Time : {:s}, Cpu temp: {:s}%, Cpu use: {}%, Mem total: {:.1f} MB, Mem use: {:.1f} MB".format(ti.strftime("%Y-%m-%d %H:%M:%S.%f"),da, cpu_use, mem_tot, mem_use)
        row = "{:s}, {:s}%, {}%, {:.1f} MB, {:.1f} MB".format(ti.strftime("%Y-%m-%d %H:%M:%S.%f"),da, cpu_use, mem_tot, mem_userow = "{:s},{:s}".format(ti.strftime("%Y-%m-%d %H:%M:%S.%f"),da)
        client.publish(MQ_TITLE,payload=row, qos=1)
        if i%freq == 0:
            print (i, row)
        time.sleep(delta)

if __name__ == "__main__":
    print ("get client")
    client = mqtt.Client("CPU_TEMP_PUB01")
    client.username_pw_set(mqconfig.mq_user, password=mqconfig.mq_password)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    print ("Try to connect {} ".format(MQ_HOST))
    client.connect(MQ_HOST, port=1883, keepalive=120)
    print ("connected {} ".format(MQ_HOST))
    client.loop_start()
    pubTempData(client)

    print ("sleep end")
    client.loop_stop()
