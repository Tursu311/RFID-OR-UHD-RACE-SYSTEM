#Program to write an increasing number to the tag if the tag is empty

#We assign the pin numbers of rst pin
pinnumbers = [20, 21]

#We set the led pins
redPin = 12
greenPin = 19
bluePin = 13

import requests
import csv
import json
from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import spidev
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

#We create the function to change the led color
def red():
    GPIO.output(redPin,GPIO.LOW)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)

def green():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.LOW)
    GPIO.output(bluePin,GPIO.HIGH)
    
def turnOff():
    GPIO.output(redPin,GPIO.HIGH)
    GPIO.output(greenPin,GPIO.HIGH)
    GPIO.output(bluePin,GPIO.HIGH)

#Is the list of runners that have passed through the checkpoint
corredors = []

#Class to manage multiple rfid readers
class RFID():
    def __init__(self, bus=0, device=0, spd=1000000):
        self.reader = SimpleMFRC522()
        self.close()
        self.boards = []
        self.bus = bus
        self.device = device
        self.spd = spd

    #Method to reinitialize the spi connection
    def reinit(self):
        self.reader.READER.spi = spidev.SpiDev()
        self.reader.READER.spi.open(self.bus, self.device)
        self.reader.READER.spi.max_speed_hz = self.spd
        self.reader.READER.MFRC522_Init()

    #Method to close the spi connection
    def close(self):
        self.reader.READER.spi.close()

    #Method to add a new board to the list of boards with its pin
    def addBoard(self, pin):
        self.boards.append(pin)

    
    #Method to read the rfid value and return it
    def read(self):
        GPIO.setmode(GPIO.BCM)
        #We assign the pin to the value of the list index
        pin = self.boards[i]
        #We set the pin as output
        GPIO.setup(pin, GPIO.OUT)
        print("Reader: " + str(i))
        self.reinit()
        uid, checkpoints = self.reader.read_no_block()
        #We set the pin as input again to avoid problems with the spi connection
        GPIO.setup(pin, GPIO.IN)
        self.close()
        sleep(0.5)
        return uid

if __name__ == "__main__":
    rfid = RFID()
    n = 0
    while n < len(pinnumbers):
        rfid.addBoard(pinnumbers[n])
        n += 1

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
        
#We read runners.csv and we create a list with the names and surnames we skip the ones assigned
with open('runners.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    names = []
    surnames = []
    for row in reader:
        if row[2] != "assigned":
            names.append(row[0])
            surnames.append(row[1])
csvfile.close()

n = 1
while True:
    i = 0
    #We iterate through the list of boards
    while i < len(rfid.boards):
        print(names[n] + " " + surnames[n])
        try:
            #We read the value of the rfid
            uid = rfid.read()
            print("UID: " + str(uid))
            if uid is not None:
                uid = str(uid)
                try:
                    print(corredors)
                    if uid not in corredors:
                        #We insert the new entry sending the data through post request
                        try:
                            #We create the data to send
                            data = {'user': 'dbuser', 
                                    'password': 'dbpassword', 
                                    'uid': uid, 
                                    'name': names[n],
                                    'surname': surnames[n],
                            }
                            json_data = json.dumps(data)
                            headers = {'Content-type': 'application/json'}
                            print(data)
                            #We send the data
                            r = requests.post("https://yoururl/php/getdata.php", verify=False, data=json_data, headers=headers)
                            #We print the response
                            print(r.text)
                            print(r.status_code, r.reason)
                            #We add the runner to the list and the csv
                            with open('ruids.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([uid])
                                #we close the document
                                csvfile.close()
                                corredors.append(uid)
                            #We mark the runner as assigned in the csv
                            with open('runners.csv', 'r') as csvfile:
                                reader = csv.reader(csvfile)
                                lines = list(reader)
                                lines[i][2] = "assigned"
                            csvfile.close()
                            green()
                            print("The runner has been added to the database")
                            sleep(0.5)
                            turnOff()
                            n += 1
                        except:
                            red()
                            print("Method error")                      
                    else:
                        print("The runner has already passed through this checkpoint")
                        green()
                        sleep(0.5)
                        turnOff()
                except:
                    print("Error al metode")
                    red()
            else:
                print("No value")
                turnOff()
            i += 1
        except:
            print("Error al llegir el rfid")
            red()