import time
import board
import busio
import adafruit_mlx90640
import requests
import statistics
import json

FRAME_SIZE = 768
FRAME_HEIGHT = 24
FRAME_WIDTH = 32
TEMPERATURE_THRESHOLD = 34


I2C = busio.I2C(board.SCL, board.SDA, frequency=400000)

thermalCamera = adafruit_mlx90640.MLX90640(I2C)

thermalCamera.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_0_5_HZ

cameraFrame = [0] * FRAME_SIZE

DEVICE_ID = "/topics/6"
SERVER_URL="http://localhost"
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
        data = {'to': DEVICE_ID, 'notification': {'title': 'Temperature Anomaly', 'body': 'Temperature anamaly detected: {0:.1f}'.format(fahrenheit) + '°F'}, 'priority': 'high'}
        r = requests.post(FIREBASE_URL, headers=header, data=json.dumps(data))
        print(r.content)

alertObject = heatWatch()

while True:
    try:
        thermalCamera.getFrame(cameraFrame)
    except ValueError:
        continue
    
    highTemp=max(cameraFrame)
    lowTemp=min(cameraFrame)
    ambientTemp=int(statistics.median(cameraFrame))
    
    print("Max Temp Celsius: {0:0.2f} \nMin Temp Celsius: {1:0.2f}".format(max(cameraFrame), min(cameraFrame)))
    print("Ambient(median) temperature: " + str(ambientTemp))

   #ambientTempUpdate = requests.get(url=SERVER_URL, params= str(int(ambientTemp)))

    if(highTemp >= TEMPERATURE_THRESHOLD):
        alertObject.heatAlert(highTemp)
    
    time.sleep(5)
