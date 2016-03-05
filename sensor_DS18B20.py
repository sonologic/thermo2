from os import listdir
from time import time
import os
from sensor import Sensor

class DS18B20Sensor(Sensor):
    #if not os.path.exists('/sys/bus/w1/devices/'+str(id)):
    #  raise Exception("No sensor with id "+str(id))
  
  @staticmethod 
  def scan():
    sensors = []
    devices = listdir('/sys/bus/w1/devices')
    for dev in devices:
      if dev[0:3]=='28-':
        sensors.append(dev)
    return sensors

  def getValue(self):
    if not os.path.exists('/sys/bus/w1/devices/'+str(self.id)):
      raise Exception("No sensor with id "+str(self.id))
    sensor = open("/sys/bus/w1/devices/"+str(self.id)+"/w1_slave")
    text = sensor.read()
    sensor.close()
    line = text.split("\n")[1]
    data = line.split(" ")[9]
    self.value = float(data[2:]) / 1000
    return temp
