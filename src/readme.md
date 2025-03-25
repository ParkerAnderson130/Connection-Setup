# Connection setup for STREAM

To change the device sending info, you need to change 3 parts of the program:

1. The set_info JSON that establishes the AWS object (Defined in parent class)
2. The upload_data JSON that tells the program what data to send to the site (Also in parent class)
3. The actual connection to the device (In main.py)

## main.py

This is main file for sending data to STREAM. It establishes a connection to whatever type of device you instantiate and sends packets to the WebSocket server on a thread until the program is stopped.