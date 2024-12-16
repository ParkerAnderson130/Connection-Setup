# Connection setup for STREAM

## main.py

This is main file for sending data to STREAM. It establishes a connection to whatever type of device you instantiate and sends packets to the WebSocket server on a thread until the program is stopped.

To change the device sending info, you need to change 3 parts of the program (They are marked by the respective number).

1. The set_info JSON that establishes the AWS object
2. The upload_data JSON that tells the program what data to send to the site
3. The actual connection to the device

## printer.py

This is the file that defines the class Printer and creates a serial connection to a 3D Printer to use GCode to request data and execute functions.

To add functionality to the printer, you can change 3 parts of the program (They are marked by the respective number).

1. The dict of valid commands recognized from the terminal in STREAM
2. The execution of the commands in the dict (This is listed in case a future user wants to have the commands extend beyond basic GCode)
3. The execution of raw GCode if the command does not exist in the dict

You can add functions as necessary, the current functions implemented are for the graph feature in STREAM:

#### getTemperature(self)
Calls "M105\n" to request base temperature

*Note: _parseTemperature(self, response) is a helper function that trims the response from the printer so the main file can extract the value only*

#### getPressure(self)
Calls "M119\n" to request base pressure

*Note: _parsePressure(self, response) is a helper function that trims the response from the printer so the main file can extract the value only*

## test-3d.py and test-ws.py
These files are test files for functions used in the other two files. These files can be manipulated as needed and do not impact the functionality of the other two.