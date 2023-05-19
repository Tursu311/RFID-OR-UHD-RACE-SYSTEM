#We assign the checkpoint_id number
checkpoint_id = 0

import datetime
import requests
import csv
import json
import RPi.GPIO as GPIO
from evdev import InputDevice
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)


#Is the list of runners that have passed through the checkpoint
corredors = []

#Class to manage UHF antenna
class UHF:
    def __init__(self, device_path):
        self.device = InputDevice(device_path)
        self.buffer = ""

    def read(self):
        self.buffer = ""
        for event in self.device.read_loop():
            if event.type == 1 and event.value == 1:
                if event.code == 28:
                    break
                else:
                    self.buffer += str(event.code)

    def close(self):
        self.device.close()


if __name__ == "__main__":
    scanner = UHF('/dev/input/event0')  # Replace with the correct device path


    try:
        with open('uids.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                corredors.append(row[0])
        csvfile.close()
    except:
        print("Error reading the CSV")
        #We create the csv
        with open('uids.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['uid', 'checkpoint_id', 'time'])
            csvfile.close()

    while True:
        try:
            scanner.read()
            uid = str(scanner.buffer)
            print(uid)
        except:
            print("Error reading the RFID")
        if uid != "" and len(uid) >= 10:
            try:
                #We check if the runner has already passed through the checkpoint
                if uid not in corredors:
                    time = datetime.datetime.now().strftime("%H:%M:%S")
                    print(time)
                    print(corredors)
                    try:
                        with open('uids.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([uid, checkpoint_id, time])
                            csvfile.close()
                            corredors.append(uid)
                    except:
                        print("Error writing to CSV")

                    try:
                        data = {
                            'user': 'dbuser',
                            'password': 'dbpassword',
                            'uid': uid,
                            'checkpoint_id': str(checkpoint_id),
                            'time': time
                        }
                        json_data = json.dumps(data)
                        headers = {'Content-type': 'application/json'}
                        print(data)
                        r = requests.post("https://yoururl/php/getdata.php", verify=False, data=json_data, headers=headers)
                        print(r.text)
                        print(r.status_code, r.reason)
                    except:
                        print("Error sending the POST")
                else:
                    print("The runner has already passed through this checkpoint")
            except:
                print("Error in the method")
        else:
            print("No value")