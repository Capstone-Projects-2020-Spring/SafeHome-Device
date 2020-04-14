import time
import board
import busio
import adafruit_mlx90640
import requests
import statistics

FRAME_SIZE = 768
FRAME_HEIGHT = 24
FRAME_WIDTH = 32
TEMPERATURE_THRESHOLD = 34


I2C = busio.I2C(board.SCL, board.SDA, frequency=400000)

thermalCamera = adafruit_mlx90640.MLX90640(I2C)

thermalCamera.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_0_5_HZ

cameraFrame = [0] * FRAME_SIZE

DEVICE_ID = "7"
SERVER_URL="http://localhost"
FIREBASE_URL="http://localhost"
FIREBASE_API_KEY="""AAAAEDDiUSU:APA91bFqIUEReFZhmk4SsGkIpIvh9Bz
                    _TTb6s9-MuPjxj9QYwEaBY6BhfxnNVNJCYtE_pngp1b
                    PsOUvQMICdK5LKwcXKcoPT-QAKXK9otinw4t13Q0FyE
                    B1dE9DSzXx59fQSZWzG_o9m"""

class heatWatch:

    def __init__(self):
        self.lastNotified = 0
        self.NOTIFICATION_INTERVAL= 60
        #self.TEMPERATURE_THRESHOLD=threshold

    def heatAlert(self, celsius):
        print("Last notified at: %0.4f\n" % self.lastNotified)

        if(self.lastNotified == 0): #first time sending the notification
            print("Anomaly detected: %0.2f\n" % celsius)
            self.lastNotified = time.time()
        if(time.time() - self.lastNotified > self.NOTIFICATION_INTERVAL):
            #if (celsius>=self.TEMPERATURE_THRESHOLD):
                #HTTP POST REQUEST GOES HERE
            print("Anomaly detected: %0.2f\n" % celsius)
            self.lastNotified = time.time()

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
