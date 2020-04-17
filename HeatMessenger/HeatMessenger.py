import time
import board
import busio
import adafruit_mlx90640
import requests
import statistics
import json
import sys

FRAME_SIZE = 768
FRAME_HEIGHT = 24
FRAME_WIDTH = 32
TEMPERATURE_THRESHOLD = 32


I2C = busio.I2C(board.SCL, board.SDA, frequency=400000)

thermalCamera = adafruit_mlx90640.MLX90640(I2C)

thermalCamera.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_0_5_HZ

cameraFrame = [0] * FRAME_SIZE

DEVICE_ID = " "
DEVICE_NAME = " "
SERVER_URL="http://198.211.109.9:8000/SafeHomeDatabase/setTemp/"
FIREBASE_URL="https://fcm.googleapis.com/fcm/send"
FIREBASE_API_KEY='AAAAEDDiUSU:APA91bFqIUEReFZhmk4SsGkIpIvh9Bz_TTb6s9-MuPjxj9QYwEaBY6BhfxnNVNJCYtE_pngp1bPsOUvQMICdK5LKwcXKcoPT-QAKXK9otinw4t13Q0FyEB1dE9DSzXx59fQSZWzG_o9m'
header = {'Content-Type': 'application/json', 'Authorization': 'key=' + FIREBASE_API_KEY}

class heatWatch:

    def __init__(self):
        self.lastNotified = 0
        self.NOTIFICATION_INTERVAL= 60
        #self.TEMPERATURE_THRESHOLD=threshold

    def heatAlert(self, celsius):
        print("Last notified at: %0.4f\n" % self.lastNotified)

        if(self.lastNotified == 0): #first time sending the notification
            print("Anomaly detected: %0.2f\n" % celsius)
            self.sendNotification(celsius)
            self.lastNotified = time.time()
        if(time.time() - self.lastNotified > self.NOTIFICATION_INTERVAL):
            print("Anomaly detected: %0.2f\n" % celsius)
            self.sendNotification(celsius)
            self.lastNotified = time.time()

    def sendNotification(self, celsius):
        fahrenheit = (celsius * 9/5) + 32 
        data = {'to':'/topics/' + DEVICE_ID, 'notification': {'title': 'Alert at Device: ' + DEVICE_NAME, 'body': 'Temperature anomaly detected: {0:.1f}'.format(fahrenheit) + '°F'}, 'priority': 'high'}
        r = requests.post(FIREBASE_URL, headers=header, data=json.dumps(data))
        print ("Sent notification to URL: ",r.url)
        print ("\n\n",r.content)

alertObject = heatWatch()

#Device ID will be pulled in as first parameter, Program will exit if not supplied
if len(sys.argv)>1:
    DEVICE_ID=sys.argv[1]
else:
    print ("Please provide Device ID as first parameter")
    sys.exit()

prevTemp=0


r1 = requests.get("http://198.211.109.9:8000/SafeHomeDatabase/getDevices/", params= {"email": "admin"})
r1_string = r1.content.decode("utf-8").split(',')

for devices in r1_string:
        device = devices.split('-')
        if(device[0] == DEVICE_ID):
                DEVICE_NAME = device[1]
                break

while True:
    try:
        thermalCamera.getFrame(cameraFrame)
    except ValueError:
        continue
    
    highTemp=max(cameraFrame)
    lowTemp=min(cameraFrame)
    ambientTemp=int(statistics.median(cameraFrame))
    
    #print("Max Temp Celsius: {0:0.2f} \nMin Temp Celsius: {1:0.2f}".format(max(cameraFrame), min(cameraFrame)))
    #print("Ambient(median) temperature: " + str(ambientTemp))
    
    
    #Checks if the room median temperature has changed
    #sends an update to the server if so
    if ambientTemp!=prevTemp:
        ambientTempUpdate = requests.get(SERVER_URL, params= {"id":DEVICE_ID,"temp":str(int(ambientTemp))})
        prevTemp=ambientTemp
        print(ambientTempUpdate.url)
        print("Status Code: " + str(ambientTempUpdate.status_code))
    if(highTemp >= TEMPERATURE_THRESHOLD):
        alertObject.heatAlert(highTemp)
    
    time.sleep(5)
