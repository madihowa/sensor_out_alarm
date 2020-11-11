from Adafruit_BME280 import *
from time import sleep
from datetime import datetime
import paho.mqtt.publish as publish
sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
MQTT_SERVER = "10.191.12.7"
MQTT_PATH = "test_channel"
from alarm_system import Emailer

def email(emailList, smsList, subjectLine, emailContent):
    sender = Emailer(emailList, smsList, subjectLine, emailContent)
    sender.alert()

def text(emailList, smsList, subjectLine, emailContent):
    sender = Emailer(emailList, smsList, subjectLine, emailContent)
    sender.alert_text()   

"""
IDEA FOR IMPLEMENTING STOPPING OF REPETITIVE MAILS/TEXT:
        1) record time when first email/text is sent
        2) using the recorded time calculate the time at which you'd want to stop sending emails. for example:
                a) first email at 10:15 PM, we want to stop sending emails if there is 3 successively, so emails after 10:15 + 3(15) = 11:00 PM must be stopped.
        3) record the reason of email, i.e. temp/humidity/pressure went out of bounds
        4) once the condition for stopping emails are met - 3 successive readings had the same issue - phase out the notifications 
"""

def checkData(thermvar, tMin, tMax, hMin, hMax, pMin, pMax ):
    temp = thermvar[0]
    humid = thermvar[1]
    pressure = thermvar[2]
    emailList = ["nural.akchurin@ttu.edu","andrew.whitbeck@ttu.edu", "sonaina.undleeb@ttu.edu", "madison.howard@ttu.edu", "vladimir.kuryatkov@ttu.edu"]
    smsList = ['8066321401@vtext.com', '8064706698@txt.att.net', '4103873814@tmomail.net', '8067907444@sms.mycricket.com']
    subjectLine = "Alert from APDL Test"        
    if temp < tMin:
       emailContent = "FROM CLEAN ROOM D: Temp less than {} degrees F. The temp reading was {} F, humidity was {} percent and pressure was {} kPa ".format(tMin, temp, humid, pressure)
       email(emailList, smsList, subjectLine, emailContent)
       text(emailList, smsList, subjectLine, emailContent)

    elif temp > tMax:
       emailContent = "FROM CLEAN ROOM D: Temp more than {} degrees F. The temp reading was {} F, humidity was {} percent and pressure was {} kPa ".format(tMax, temp, humid, pressure)
       email(emailList, smsList, subjectLine, emailContent)
       text(emailList, smsList, subjectLine, emailContent)

    else:
        pass

    if humid < hMin:
       emailContent = "FROM CLEAN ROOM D: Humidity was less than {} percent. The temp reading was {} F, humidity was {} percent and pressure was {} kPa ".format(hMin, temp, humid, pressure)
       email(emailList, smsList, subjectLine, emailContent)
       text(emailList, smsList, subjectLine, emailContent)

    elif humid > hMax:
       emailContent = "FROM CLEAN ROOM D: Humidity was more than {} percent. The temp reading was {} F, humidity was {} percent  and pressure was {} kPa ".format(hMax, temp, humid, pressure)
       email(emailList, smsList, subjectLine, emailContent)
       text(emailList, smsList, subjectLine, emailContent)

    else:
        pass

    if pressure < pMin:
       emailContent = "FROM CLEAN ROOM D: Pressure was less than {} kPa. The temp reading was {} F, humidity was {} percent and pressure was {} kPa ".format(pMin, temp, humid, pressure) 
       email(emailList, smsList, subjectLine, emailContent)
       text(emailList, smsList, subjectLine, emailContent)

    elif pressure > pMax:
       emailContent = "FROM CLEAN ROOM D: Pressure was more than {} kPa. The temp reading was {} F, humidity was {} percent and pressure was {} kPa ".format(pMax, temp, humid, pressure)
       email(emailList, smsList, subjectLine, emailContent)
       text(emailList, smsList, subjectLine, emailContent)

    else:
        pass

def round_sf(variable, sig_fig):
    return round(variable,sig_fig-len(str(variable)))

while True:
        
    file1=open("weatherlog.txt","a")
    degrees = sensor.read_temperature()
    humidity = sensor.read_humidity()
    pascals = sensor.read_pressure()

    degrees = round_sf(degrees, 3)
    humidity  = round_sf(humidity, 3)
    pascals = round_sf(pascals, 3)

    KPA = (pascals) / 1000
    Faren = (degrees*9/5)+32
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y-%H:%M:%S ")
    file1.write(dt_string)
    print (dt_string)
        
    print('Temp      = {0:0.3f}'.format(Faren))
    print('Humidity  = {0:0.6f}'.format(humidity))
    print('Pressure  = {0:0.4f}'.format(KPA))
        
    publish.single("Temp(D)", Faren, hostname=MQTT_SERVER)
    publish.single("Pressure(D)", KPA, hostname=MQTT_SERVER)
    publish.single("Humidity(D)", humidity, hostname=MQTT_SERVER)
        
    file1.write('Temp= {0:0.3f}F '.format(Faren) )
    file1.write(' Humidity= {0:0.6f}%'.format(humidity) )
    file1.write(' Pressure= {0:0.4f}inHg \n'.format(KPA))
        
    thermvar = [Faren, humidity, KPA] 
    checkData(thermvar, 60, 80, 10, 60, 0, 10000)

    sleep(600) 
