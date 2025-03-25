import serial
import time

class c:  # Colors for message headers, shortened to c for readability
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

class Printer:
    def __init__(self, port, baudrate=115200, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connection = None

        ### 1. CHANGE TO ADD VALID COMMANDS ###
        self.commands = {
            "LEVEL": "G29",  # -> Levels printer base
        }
        ###

    def connect(self):
        try:
            self.connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)
            print(c.GREEN + f"CONNECTED: " + c.END + f"{self.port} at {self.baudrate} baud")
        except serial.SerialException as e:
            print(c.RED + "SERIAL EXCEPTION: " + c.END + str(e))

    def execute_command(self, command):
        command = command.upper()

        ### 2. PREDEFINED COMMANDS ###
        if command in self.commands:
            gcode_command = self.commands[command] + "\n"
            print(c.GREEN + f"SENT: " + c.END + f"{gcode_command.strip()}")
        ###
        ### 3. RAW GCODE ###
        else:
            gcode_command = command + "\n"
            print(c.GREEN + f"SENT: " + c.END + f"{gcode_command.strip()}")
        ###
        if self.connection and self.connection.is_open:
            self.connection.write(gcode_command.encode())

            response = self.connection.readline().decode().strip()
            print(c.BLUE + f"RECEIVED: " + c.END + f"{response}")
            return response
        else:
            print(c.RED + "PRINTER NOT CONNECTED" + c.END)
            return "PRINTER NOT CONNECTED"

    def getTemperature(self):
        if self.connection and self.connection.is_open:
            gcode_command = "M105\n"  # Requests printer temperature
            self.connection.write(gcode_command.encode())
            print(c.GREEN + f"SENT: " + c.END + f"{gcode_command.strip()}")

            response = self.connection.readline().decode().strip()
            print(c.BLUE + f"RECEIVED: " + c.END + f"{response}")
            
            temp = self._parseTemperature(response)
            return temp
        else:
            print(c.RED + "PRINTER NOT CONNECTED" + c.END)
            return None

    def _parseTemperature(self, response):
        # Format is "ok T:22.0 /0.0"
        try:
            if "T:" in response:
                temp_str = response.split("T:")[1].split(" ")[0]
                return float(temp_str)
        except (IndexError, ValueError):
            print(c.RED + "FAILED TO PARSE TEMPERATURE FROM RESPONSE" + c.END)
        return None
    
    def getPressure(self):
        if self.connection and self.connection.is_open:
            gcode_command = "M119\n"  # Requests printer pressure
            self.connection.write(gcode_command.encode())
            print(c.GREEN + f"SENT: " + c.END + f"{gcode_command.strip()}")

            response = self.connection.readline().decode().strip()
            print(c.BLUE + f"RECEIVED: " + c.END + f"{response}")
            
            pressure = self._parsePressure(response)
            return pressure
        else:
            print(c.RED + "PRINTER NOT CONNECTED" + c.END)
            return None

    def _parsePressure(self, response):
        # Format is "Pressure: <value>"
        try:
            if "Pressure:" in response:
                pressure_str = response.split("Pressure:")[1].strip()
                return float(pressure_str)
        except (IndexError, ValueError):
            print(c.RED + "FAILED TO PARSE PRESSURE FROM RESPONSE" + c.END)
        return None

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            print(c.GREEN + "CLOSED PRINTER CONNECTION" + c.END)