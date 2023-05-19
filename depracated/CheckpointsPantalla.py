#
#
#     IMPORTANT!!
#Non updated with the latest changes see CheckpointsLedRemotPost.py
#
#


import datetime
from RPLCD import CharLCD
from time import sleep
import RPi.GPIO as GPIO
import mysql.connector as mysql
from mfrc522 import SimpleMFRC522
import spidev
GPIO.setmode(GPIO.BCM)

#We assign the checkpoint_id number
checkpoint_id = 3

mydb = mysql.connect(
  host="localhost",
  user="dbuser",
  password="pi",
  database="race"
)
mycursor = mydb.cursor(buffered=True)
#Class to manage multiple NFC readers
class NFC():
    #Constructor of the class 
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

    
    def read(self):
        GPIO.setmode(GPIO.BCM)
        #We assign the pin to the value of the list index
        pin = self.boards[i]
        GPIO.setup(pin, GPIO.OUT)
        print(i)
        self.reinit()
        cid, val = self.reader.read_no_block()
        GPIO.setup(pin, GPIO.IN)
        self.close()
        print(val)
        sleep(0.5)
        GPIO.cleanup()
        return val

    def write(self, rid, value):
        if not self.selectBoard(rid):
            return False

        self.reinit()
        self.reader.write_no_block(value)
        self.close()
        return True

if __name__ == "__main__":
    nfc = NFC()
    nfc.addBoard(20)
    nfc.addBoard(21)
    
while True:
    #We have to read nfc value and send it to the databse alongside the checkpoint_id number and the time, we have to check if the value is already in the database
    i = 0
    #We read the value of the nfc
    while i < len(nfc.boards):
        nfcvalue = nfc.read()
        #We check if the runnername has an entry for the checkpoint_id
        mycursor.execute("SELECT * FROM times WHERE DNI = %s AND checkpoint_id = %s", (nfcvalue, checkpoint_id))
        
        if nfcvalue is not None:
            if mycursor.rowcount == 0:
                #We insert the new entry
                time = datetime.datetime.now()
                sql = "INSERT INTO times (DNI, checkpoint_id, checkpoint_time) VALUES (%s, %s, %s)"
                val = (nfcvalue, checkpoint_id, time)
                mycursor.execute(sql, val)
                mydb.commit()
                print(mycursor.rowcount, "record inserted.")
                #We display runner name, and checkpoint time on the lcd
                lcd = CharLCD(numbering_mode=GPIO.BCM, cols=16, rows=2, pin_rs=25, pin_e=24, pins_data=[23,17,18,22])
                lcd.clear()
                sleep(0.5)
                lcd.write_string("Runner: " + str(nfcvalue) + "\nTime: " + str(time))
                sleep(4)
                lcd.clear()
            else:
                print("The runner has already passed through this checkpoint")
        else:
            print("No value")
        i += 1