import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# Create an object of the class MFRC522
reader = SimpleMFRC522()

# Function to write runner name to RFID tag
def write():
    runner_name = input("Enter data: ")
    
    # Write runner name to tag
    reader.write(runner_name)
    print("Runner name written to card")


# Function to read data from RFID tag
def read_data():
    # Read data from tag
    id, text = reader.read()
    print("ID: %s \nData: %s" % (id, text))


# Menu
while True:
    print("1. Write")
    print("2. Read uid and data")
    print("3. Exit")
    option = input("Choose an option: ")
    
    if option == "1":
        write()
    elif option == "2":
        read_data()
    elif option == "3":
        GPIO.cleanup()
        break
    else:
        print("Invalid option")
