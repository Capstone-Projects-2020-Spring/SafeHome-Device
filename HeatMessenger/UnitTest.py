import unittest
import requests
import sys

DEVICE_ID = ""
SERVER_URL="http://198.211.109.9:8000/SafeHomeDatabase"
CODE = 0
PASS_CODE = 200


class test(unittest.TestCase):
    print("Testing")

    def test_getDevice(self):
        r = requests.get(SERVER_URL + "/getDevices/", params= {"email": "UnitTest"})
        CODE = r.status_code
        self.assertEqual(CODE, PASS_CODE)
    def test_setTemp(self):
        r = requests.get(SERVER_URL + "/setTemp/", params={"id":6, "temp": "25"})
        CODE = r.status_code
        self.assertEqual(CODE, PASS_CODE)

if __name__ == '__main__':
    unittest.main()
        