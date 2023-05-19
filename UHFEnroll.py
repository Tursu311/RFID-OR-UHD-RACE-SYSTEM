#We read the uid from the rfid, then we grab the row from the csv and write it to the database, we make a second csv with the uid to prevent from writing it again

import requests
import csv
import json
import RPi.GPIO as GPIO
from evdev import InputDevice
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)


#Is the list of runners that have passed through the checkpoint
corredors = []

#Class to manage multiple NFC readers
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

#We open the csv with the uids that already passed
    try:
        with open('ruids.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                corredors.append(row[0])
        csvfile.close()
    except:
        print("Error reading the CSV")
        #We create the csv
        with open('ruids.csv', 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['uid'])
            csvfile.close()
            
    #We read runners.csv and we create a list with the names and surnames we the ones assigned
    with open('runners.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        names = []
        surnames = []
        nrow = 0
        for row in reader:
            if row[2] != "assigned":
                names.append(row[0])
                surnames.append(row[1])

    csvfile.close()
        
    i = 0
    while i < len(names):
        print(names[i] + " " + surnames[i])
        try:
            scanner.read()
            uid = str(scanner.buffer)
            print(uid)
            if uid != "" and len(uid) >= 10:
                print(corredors)
                if uid not in corredors:
                    try:
                        data = {
                            'user': 'dbuser',
                            'password': 'dbpassword',
                            'uid': uid,
                            'name': names[i],
                            'surnames': surnames[i],
                        }
                        json_data = json.dumps(data)
                        headers = {'Content-type': 'application/json'}
                        print(data)
                        r = requests.post("https://yoururl/php/enrollar.php", verify=False, data=json_data, headers=headers)
                        print(r.text)
                        print(r.status_code, r.reason)
                        with open('ruids.csv', 'a') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([uid])
                        csvfile.close()
                        corredors.append(uid)
                        #We mark the runner as assigned in the csv, we have to search the name and surname 
                        with open('runners.csv', 'r') as csvfile:
                            reader = csv.reader(csvfile)
                            data = []
                            for row in reader:
                                data.append(row)
                        csvfile.close()
                        with open('runners.csv', 'w') as csvfile:
                            writer = csv.writer(csvfile)
                            for row in data:
                                if row[0] == names[i] and row[1] == surnames[i]:
                                    row[2] = "assigned"
                                writer.writerow(row)
                        csvfile.close()
                        i += 1
                    except:
                        print("Method error")
                else:
                    print("The runner has already registered")
            else:
                print("No value")
        except:
            print("Error reading the RFID")
        