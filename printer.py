# printer.py

import serial
import time

class Printer:
    def __init__(self, port, baudrate=115200, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

    def connect(self):
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)
            print(f"Connected to {self.port} at {self.baudrate} baud.")
        except serial.SerialException as e:
            print(f"Serial exception: {e}")

    def getTemperature(self):
        if self.connection and self.connection.is_open:
            gcode_command = "M105\n" # Requests the current temperature 
            self.connection.write(gcode_command.encode())
            print(f"Sent: {gcode_command.strip()}")

            response = self.connection.readline().decode().strip()
            print(f"Received: {response}")
            # Format is "ok T:22.0 /0.0" 
            # https://3dprinting.stackexchange.com/questions/1555/access-temperature-sensor-data-of-3d-printer-via-serial-connection
            temp = self._parseTemperature(response)
            return temp
        else:
            print("Printer not connected.")
            return None

    def _parseTemperature(self, response):
        try:
            if "T:" in response:
                temp_str = response.split("T:")[1].split(" ")[0]
                return float(temp_str)
        except (IndexError, ValueError):
            print("Failed to parse temperature from response.")
        return None

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            print("Closed printer connection.")
