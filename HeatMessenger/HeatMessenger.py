import time
import board
import busio
import adafruit_mlx90640
import requests
import statistics

FRAME_SIZE = 768
FRAME_HEIGHT = 24
FRAME_WIDTH = 32



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
    lastNotified=0

    def __init__(self, threshold=38, interval=60):
        lastNotified = time.time()
        self.NOTIFICATION_INTERVAL=interval
        self.TEMPERATURE_THRESHOLD=threshold

    #def heatAlert(self, celsius):
        #if (time.time()- self.lastNotified > self.NOTIFICATION_INTERVAL):
            #if (celsius>=self.TEMPERATURE_THRESHOLD):
                #HTTP POST REQUEST GOES HERE
            
        
    



alertObject = heatWatch()


while True:
    try:
        thermalCamera.getFrame(cameraFrame)
    except ValueError:
        continue
    
    
    
    highTemp=max(cameraFrame)
    lowTemp=min(cameraFrame)
    ambientTemp=int(statistics.median(cameraFrame))
    
    print("Max Temp Celsius: {0:0.2f} \nMin Temp Celsius: {1:0.2f}\n".format(max(cameraFrame), min(cameraFrame)))
    
    print("Ambient(median) temperature: " + str(ambientTemp))
    ambientTempUpdate = requests.get(url=SERVER_URL, params= str(int(ambientTemp)))
    
    
    
    time.sleep(5)
