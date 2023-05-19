#We assign the checkpoint_id number
checkpoint_id = 0
#We assign the pin numbers of rst pin
pinnumbers = [20, 21]
#We set the led pins
redPin = 12
greenPin = 19
bluePin = 13

import datetime
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
        return uid, checkpoints

    #Method to grab the tag value and append to it the checkpoint_id
    def write(self, checkpoints):
        GPIO.setmode(GPIO.BCM)
        #We assign the pin to the value of the list index
        pin = self.boards[i]
        #We set the pin as output
        GPIO.setup(pin, GPIO.OUT)
        print("Reader: " + str(i))
        self.reinit()
        #We add the checkpoint_id to the tag value
        checkpoints = str(checkpoints)[0:checkpoint_id] + str(checkpoint_id)
        #We write the new value to the tag
        self.reader.write_no_block(checkpoints)
        #We set the pin as input again to avoid problems with the spi connection
        GPIO.setup(pin, GPIO.IN)
        self.close()
        sleep(0.5)

if __name__ == "__main__":
    rfid = RFID()
    n = 0
    while n < len(pinnumbers):
        rfid.addBoard(pinnumbers[n])
        n += 1

try:
    with open('uids.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        #We iterate through the file and add the runners to the dictionary
        for row in reader:
            #We add the runners to the list
            corredors.append(row[0])
        #We close the file
        csvfile.close()
except:
    print("Error al llegir el csv")
    #We create the csv file
    with open('uids.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        #We add the headers
        writer.writerow(['uid', 'checkpoint_id', 'time'])
        csvfile.close()


while True:
    i = 0
    #We iterate through the list of boards
    while i < len(rfid.boards):
        try:
            #We read the value of the rfid
            uid, checkpoints = rfid.read()
            print("UID: " + str(uid))
            print("Checkpoints: " + str(checkpoints))
            if uid is not None:
                uid = str(uid)
                try:
                    rfid.write(checkpoints)
                    print(corredors)
                    if uid not in corredors:
                        #We grab the current time withouth days
                        time = datetime.datetime.now().strftime("%H:%M:%S")
                        print(time)
                        #We add the runner, checkpoint and time, to the list and the csv
                        try:
                            with open('uids.csv', 'a') as csvfile:
                                writer = csv.writer(csvfile)
                                writer.writerow([uid, checkpoint_id, time])
                                #we close the document
                                csvfile.close()
                                corredors.append(uid)
                                green()
                                sleep(0.5)
                                turnOff()
                        except:
                            print("Error en escriurre al csv")
                        #We insert the new entry sending the data through post request
                        try:
                            #We create the data to send
                            data = {'user': 'dbuser', 
                                    'password': 'dbpassword', 
                                    'uid': uid, 
                                    'checkpoint_id': str(checkpoint_id),
                                    'time': time}
                            json_data = json.dumps(data)
                            headers = {'Content-type': 'application/json'}
                            print(data)
                            #We send the data
                            r = requests.post("https://yoururl/php/getdata.php", verify=False, data=json_data, headers=headers)
                            #We print the response
                            print(r.text)
                            print(r.status_code, r.reason)
                        except:
                            print("Error en enviar el post")                                                        
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