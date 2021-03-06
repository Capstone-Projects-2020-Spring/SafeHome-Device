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

#temp threshold now in fahrenheit
UPPER_TEMPERATURE_THRESHOLD = 85
LOWER_TEMPERATURE_THRESHOLD = 45
VARIANCE_CHANGE_THRESHOLD = 0.5
NOTIFICATION_INTERVAL= 60


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

    def heatAlert(self, fahrenheit):

        if(self.lastNotified == 0): #first time sending the notification
            self.sendNotification(fahrenheit)
            self.lastNotified = time.time()
        elif(time.time() - self.lastNotified > NOTIFICATION_INTERVAL):
            
            self.sendNotification(fahrenheit)
            self.lastNotified = time.time()
        else:
            return
            
        print(("Anomaly of %0.2f detected at " % fahrenheit)+time.strftime("%X, %x",time.localtime(self.lastNotified)))

    def sendNotification(self, fahrenheit):
        data = {'to':'/topics/' + DEVICE_ID, 'notification': {'title': 'Alert at Device: ' + DEVICE_NAME, 'body': 'Temperature anomaly detected: {0:.1f}'.format(fahrenheit) + '°F'}, 'priority': 'high'}
        r = requests.post(FIREBASE_URL, headers=header, data=json.dumps(data))
        print ("Sent notification to URL: ",r.url)
        print ("\n\n",r.content)

def CtoF(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit
    
    
        
#build reported temperatures into a single comma seperated string
def tempReportBuilder(fList):
    reportString=""+str(fList[0])
    if (len(fList) > 1):
        for item in range(len(fList)-1):
            reportString+=","
            reportString+=str(fList[item+1])
            
    print(reportString)
    return reportString
    
    
    
alertObject = heatWatch()

#Device ID will be pulled in as first parameter, Program will exit if not supplied
if len(sys.argv)>1:
    DEVICE_ID=sys.argv[1]
else:
    print ("Please provide Device ID as first parameter")
    sys.exit()

prevTemp=0
prevVar=0

#get device name that matches the device_id
r1 = requests.get("http://198.211.109.9:8000/SafeHomeDatabase/getDevices/", params= {"email": "admin1"})
r1_string = r1.content.decode("utf-8").split(',')

for devices in r1_string:
    device = devices.split('-')
    if(device[0].strip() == DEVICE_ID):
            DEVICE_NAME = device[1]
            break

while True:
    try:
        thermalCamera.getFrame(cameraFrame)
    except ValueError:
        continue
    highTemp=CtoF(int(max(cameraFrame)))
    lowTemp=CtoF(int(min(cameraFrame)))
    ambientTemp=CtoF(int(statistics.median(cameraFrame)))
    tempVariance=statistics.variance(cameraFrame)
    
    
    if ((prevTemp==0)or(tempVariance==0)):
        prevTemp=ambientTemp
        prevVar=tempVariance
        prevTempReport=""
        
    
    print("Variance: {0:0.3f}".format(tempVariance))
    print(DEVICE_NAME)
    
    #this line controls what order temps are reported in
    tempReport=tempReportBuilder([highTemp,ambientTemp,lowTemp])
    
    #Checks if the room median temperature has changed
    #sends an update to the server if so
    if (abs(tempVariance-prevVar)>=VARIANCE_CHANGE_THRESHOLD):
        print("Variance has changed notably, by {0:02f}".format(tempVariance-prevVar))
        prevVar=tempVariance
    if tempReport!=prevTempReport:
        tempUpdate = requests.get(SERVER_URL, params= {"id":DEVICE_ID,"temp":tempReport})
        prevTempReport=tempReport
        print(tempUpdate.url)
        print("Status Code: " + str(tempUpdate.status_code))
    if(highTemp >= UPPER_TEMPERATURE_THRESHOLD):
        alertObject.heatAlert(highTemp)
    if (lowTemp<= LOWER_TEMPERATURE_THRESHOLD):
        alertObject.heatAlert(lowTemp)
    
    time.sleep(5)