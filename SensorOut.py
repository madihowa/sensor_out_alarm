from Adafruit_BME280 import *
from time import sleep
from datetime import datetime
import paho.mqtt.publish as publish
sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
MQTT_SERVER = "10.191.12.7"
MQTT_PATH = "test_channel"
from alarm_system import Emailer

def email(emailList, subjectLine, emailContent):
    sender = Emailer(emailList, subjectLine, emailContent)
    sender.alert()
   
def checkData(thermvar, tMin, tMax, hMin, hMax, pMin, pMax ):
    temp = thermvar[0]
    humid = thermvar[1]
    pressure = thermvar[2]
    if temp < tMin:
       emailList = ["nural.akchurin@ttu.edu","andrew.whitbeck@ttu.edu", "sonaina.undleeb@ttu.edu"]
       subjectLine = "Alert from APDL Test"
       emailContent = "Temp less than {} degrees".format(tMin)
       email(emailList, subjectLine, emailContent)
    elif temp > tMax:
       emailList = ["nural.akchurin@ttu.edu","andrew.whitbeck@ttu.edu", "sonaina.undleeb@ttu.edu"]
       subjectLine = "Alert from APDL Test"
       emailContent = "Temp exceeded {} degrees".format(tMax)
       email(emailList, subjectLine, emailContent)
    else:
        pass

    if humid < hMin:
       emailList = ["nural.akchurin@ttu.edu", "andrew.whitbeck@ttu.edu", "sonaina.undleeb@ttu.edu"]
       subjectLine = "Alert from APDL Test"
       emailContent = "Humidity less than {} humidity".format(hMin)
       email(emailList, subjectLine, emailContent)
    elif humid > hMax:
       emailList = ["nural.akchurin@ttu.edu","andrew.whitbeck@ttu.edu", "sonaina.undleeb@ttu.edu"]
       subjectLine = "Alert from APDL Test"
       emailContent = "Humidity exceeded {} humidity".format(hMax)
       email(emailList, subjectLine, emailContent)
    else:
        pass

    if pressure < pMin:
       emailList = ["nural.akchurin@ttu.edu", "andrew.whitbeck@ttu.edu", "sonaina.undleeb@ttu.edu"]
       subjectLine = "Alert from APDL Test"
       emailContent = "Pressure less than {} KPA".format(pMin)
       email(emailList, subjectLine, emailContent)
    elif pressure > pMax:
       emailList = ["nural.akchurin@ttu.edu","andrew.whitbeck@ttu.edu", "sonaina.undleeb@ttu.edu"]
       subjectLine = "Alert from APDL Test"
       emailContent = "Pressure exceeded {} KPA".format(pMax)
       email(emailList, subjectLine, emailContent)
    else:
        pass


while True:
    
    file1=open("weatherlog.txt","a")
    degrees = sensor.read_temperature()
    humidity = sensor.read_humidity()
    pascals = sensor.read_pressure()
    KPA = (pascals) / 1000
    Faren = (degrees*9/5)+32
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y-%H:%M:%S ")
    file1.write(dt_string)
    print (dt_string)
    
    print('Temp      = {0:0.3f}'.format(Faren))
    print('Humidity  = {0:0.6f}'.format(humidity))
    print('Pressure  = {0:0.4f}'.format(KPA))
    
    publish.single("Temp(A)", Faren, hostname=MQTT_SERVER)
    publish.single("Pressure(A)", KPA, hostname=MQTT_SERVER)
    publish.single("Humidity(A)", humidity, hostname=MQTT_SERVER)
    
    file1.write('Temp= {0:0.3f}F '.format(Faren) )
    file1.write(' Humidity= {0:0.6f}%'.format(humidity) )
    file1.write(' Pressure= {0:0.4f}inHg \n'.format(KPA))
    
    thermvar = [Faren, humidity, KPA] 
    checkData(thermvar, 68, 72, 30, 50, 0, 10000)

    sleep(900)
   
