Race Control Systems
====================

This repository contains the final project of my ASIX training cycle, which consists of systems for managing and tracking the timing and checkpoints of a running race using RFID and UHF technology. 

Directory Structure
-------------------

The repository is structured as follows:

*   `database.sql`: SQL file containing the database schema for the race control system. It includes two tables:
    
    *   `runners`: Stores information about the runners and their associated tag UID.
    *   `checkpoints`: Tracks the UID, checkpoint, and time for each runner.
*   `TestPost.py`: For testing the post functionality.
    
*   `RC522CheckpointLedPost.py`: For interacting with the RC522 RFID reader. It writes the current checkpoint to the tag, writes the UID, checkpoint, and time to a CSV file, and sends the data via POST to a server. [Flowchart](/img/rc522Flowchart.png)
    
*   `RC522Debug.py`: For reading and writing data with the RC522 RFID reader.
    
*   `RC522Enroll.py`: For enrolling RFID tags with the RC522 reader.
    
*   `UHFCheckpointPost.py`: For interacting with the UHF antena. It writes the UID, checkpoint, and time to a CSV file and sends the data via POST to the server. [Flowchart](/img/uhfFlowchart.png)
    
*   `UHFEnroll.py`: For enrolling UHF tags.
    

### Deprecated

The following files are deprecated and no longer actively used in the project:

*   `CheckpointsLedRemotSQL.py`: Deprecated For remote SQL communication and controlling an LED.
    
*   `CheckpointsPantalla.py`: Deprecated For controlling LED displays at checkpoints.
    

### PHP

*   `getdata.php`: Used to receive the POST request from Python and add the data to the database.
    
*   `global.php`: Used to display an ordered table with all the runners, their last checkpoint, and the time since they started.
    
*   `index.html`: Basic HTML file that allows the user to select whether they want to see the general table or their personal times.
    
*   `personal.php`: For displaying specific runner times.
    
*   `TestPost.php`: For testing the post functionality.
    
*   `style.css`: CSS file for styling the HTML pages based on the Dracula theme.
    

Usage
-----

To use the race control systems, you will need a Raspberry Pi with Python and pip installed. For the UHF system, any device with USB ports can be used.

To display the data, you will set up a LAMP (Linux, Apache, MariaDB, PHP) stack on a computer that is accessible from your detection device.

Follow the steps below to set up and configure the systems:

1.  Install the necessary dependencies:
    
    *   For RFID: Install the `mfrc522` library using pip.
    *   For UHF: Install `evdev` using pip.
2.  Move the `php` folder to `/var/www/html/` on your LAMP server. Optionally, you can customize the Apache configuration.
    
3.  In both the Python scripts and PHP files, make the following changes:
    
    *   Update the database credentials (`user` and `password`) to match your MySQL configuration.
    *   Change the checkpoint number according to your race setup.
    *   Modify the URL of the POST request to match your server's endpoint.
4.  For the RFID system:
    
    *   Connect the RC522 readers to the Raspberry Pi's GPIO pins according to the provided [Schema](/img/rpischema.png). You can use a protoboard and cables to connect them. RST cables can go in any of the available GPIO pins.
    *   Optionally, connect an RGB LED for visual indications.
5.  For the UHF system:
    
    *   Identify the UHF reader device by checking the `/dev/input/eventX` file associated with it.
6.  Open the corresponding Python script (`RC522CheckpointLedPost.py` or `UHFCheckpointPost.py`) and update the configurations as needed:
    
    *   For RFID: Update the reader pins to match the GPIO pins you connected the RC522 readers to.
    *   For UHF: Update the device configuration with the correct `/dev/input/eventX` file. You can check it by connecting the device and running `sudo dmseg`.
7.  Enroll the tags you want to use with the system by running the corresponding Python script (`RC522Enroll.py` or `UHFEnroll.py`). Remeber to create a CSV file with the runner idalu, name, surnames, also add an "assigned" header along them that will be empty till you start enrolling the tags.
8.  Execute the chosen Python script, and the data will be displayed on `/php/global.php` in your LAMP setup.
    

Contributing
------------

Contributions to this project are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

License
-------

This project is licensed under the [GPL-3.0 License](LICENSE). Please see the LICENSE file for more details.

---
