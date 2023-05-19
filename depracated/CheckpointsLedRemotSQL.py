#
#
#     IMPORTANT!!
#Non updated with the latest changes see CheckpointsLedRemotPost.py
#
#

import datetime
from time import sleep
import RPi.GPIO as GPIO
import mysql.connector as mysql
from mfrc522 import SimpleMFRC522
import spidev
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
redPin = 12
greenPin = 19
bluePin = 13
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(bluePin,GPIO.OUT)

#We assign the checkpoint_id number
checkpoint_id = 3

#We create the database connection
mydb = mysql.connect(
  host="localhost",
  user="dbuser",
  password="pi",
  database="race"
)
mycursor = mydb.cursor(buffered=True)

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

#Class to manage multiple NFC readers
class NFC():
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

    #Method to add a new board to the list of boards with its readerid and pin
    def addBoard(self, pin):
        self.boards.append(pin)

    
    #Method to read the nfc value and return it
    def read(self):
        GPIO.setmode(GPIO.BCM)
        #We assign the pin to the value of the list index
        pin = self.boards[i]
        #We set the pin as output
        GPIO.setup(pin, GPIO.OUT)
        print("Reader: " + str(i))
        self.reinit()
        cid, val = self.reader.read_no_block()
        #We set the pin as input again to avoid problems with the spi connection
        GPIO.setup(pin, GPIO.IN)
        self.close()
        sleep(0.5)
        return val

    #Method to grab the tag value and append to it the checkpoint_id
    def write(self, val, checkpoints):
        GPIO.setmode(GPIO.BCM)
        #We assign the pin to the value of the list index
        pin = self.boards[i]
        #We set the pin as output
        GPIO.setup(pin, GPIO.OUT)
        print(i)
        self.reinit()
        #We add the checkpoint_id to the tag value
        nfcvalue = str(val) + str(checkpoints)[0:checkpoint_id] + str(checkpoint_id)
        #We write the new value to the tag
        self.reader.write_no_block(nfcvalue)
        #We set the pin as input again to avoid problems with the spi connection
        GPIO.setup(pin, GPIO.IN)
        self.close()
        sleep(0.5)

if __name__ == "__main__":
    nfc = NFC()
    nfc.addBoard(20)
    nfc.addBoard(21)

 
    while True:
        #We have to read nfc value and send it to the databse alongside the checkpoint_id number and the time, we have to check if the value is already in the database
        i = 0
        #We read the value of the nfc
        while i < len(nfc.boards):
            try:
                nfcvalue = nfc.read()
            except:
                print("Error")
                red()
            print(nfcvalue)
            if nfcvalue is not None:
                #We grab the passed checkpoints string
                checkpoints = str(nfcvalue)[10:]
                #We grab the DNI value from nfcvalue
                nfcvalue = str(nfcvalue)[0:10]
                try:
                    #We write the checkpoint_id to the nfc tag in case the conexion to the database fails
                    nfc.write(nfcvalue, checkpoints)
                    mycursor.execute("SELECT * FROM times WHERE DNI = %s AND checkpoint_id = %s", (nfcvalue, checkpoint_id))
                    time = datetime.datetime.now()
                    if mycursor.rowcount == 0:
                        #We insert the new entry
                        sql = "INSERT INTO times (DNI, checkpoint_id, checkpoint_time) VALUES (%s, %s, %s)"
                        val = (nfcvalue, checkpoint_id, time)
                        mycursor.execute(sql, val)
                        try:
                            mydb.commit()
                            print(mycursor.rowcount, "record inserted.")
                            green()
                        except:
                            mydb.rollback()
                            red()
                    else:
                        print("The runner has already passed through this checkpoint")
                        green()
                        sleep(0.5)
                        turnOff()
                except:
                    print("Error")
                    red()
            else:
                print("No value")
                turnOff()
            i += 1
