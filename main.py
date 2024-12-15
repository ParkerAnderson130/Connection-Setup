# main.py

import json
import os
import random
import time
import threading
import certifi
from dotenv import load_dotenv
import ssl
import websocket
import sys

from printer import Printer

class c:  # Colors for message headers, shortened to c for readability
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

load_dotenv()
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Global running flag
running = True

# WebSocket functions
def on_message(ws, message):
    print(c.BLUE + "MESSAGE: " + c.END + message)

    try:
        data = json.loads(message)
        
        # Check if the message is an action
        if "action" not in data:
            return

        # If action is 'send_command', execute the command
        if data.get("action") == "send_command":
            # Get the command from the message
            command = data.get("command")

            if command:
                print(c.GREEN + "EXECUTING COMMAND: " + c.END + command)
                response = printer.execute_command(command)
                print(c.BLUE + "RESPONSE: " + c.END + response)
            else:
                print(c.RED + "ERROR: " + c.END + "No 'command' field found in the message.")
        else:
            return

    except Exception as e:
        print(c.RED + f"ERROR: {str(e)}" + c.END)


def on_error(ws, error):
    print(c.RED + "ERROR: " + c.END + str(error))

def on_close(ws, close_status_code, close_msg):
    print(c.RED + "CLOSED: " + c.END + f"{close_status_code}, message: {close_msg}")

def on_open(ws):
    print(c.GREEN + "CONNECTED" + c.END)
    # Start a thread to send upload_data messages
    threading.Thread(target=send_multiple_messages, args=(ws,)).start()

def send_multiple_messages(ws):
    global running

    ### 1. CHANGE DEVICE SPECIFIC INFORMATION HERE ###
    set_info = {
        "action": "set_info",
        "display_name": "UGA Printer",
        "machine_type": "3D_PRINTER",
        "gcode": True,
        "commands": {
            "level": {
                "description": "Levels the printer base",
                "usage": "level"
            }
        },
        "sensors": {
            "bed_accelerometer": {
                "display_name": "Bed Accelerometer",
                "sensor_type": "ACCELEROMETER",
                "metrics": {
                    "meters_per_second_squared_x": {},
                    "meters_per_second_squared_y": {},
                    "meters_per_second_squared_z": {}
                }
            },
            "current_position": {
                "display_name": "Current Position",
                "sensor_type": "POSITION",
                "metrics": {
                    "millimeters_x": {},
                    "millimeters_y": {},
                    "millimeters_z": {}
                }
            },
            "extruder_accelerometer": {
                "display_name": "Extruder Accelerometer",
                "sensor_type": "ACCELEROMETER",
                "metrics": {
                    "meters_per_second_squared_x": {},
                    "meters_per_second_squared_y": {},
                    "meters_per_second_squared_z": {}
                }
            },
            "pressure_sensor": {
                "display_name": "Primary Pressure Sensor",
                "sensor_type": "PRESSURE",
                "metrics": {
                    "grams": {
                        "display_name": "g",
                        "byte_count": 2
                    }
                }
            },
        }
    }
    ###

    try:
        # -> Send the initial "set_info" packet
        if ws.sock and ws.sock.connected:
            ws.send(json.dumps(set_info))
            print(c.GREEN + "SENT MESSAGE: " + c.END + str(set_info))
        else:
            print(c.RED + "WEBSOCKET NOT CONNECTED" + c.END)

        # -> Send "upload_data" packets to update STREAM
        while running and ws.sock and ws.sock.connected:
            ### 2. CHANGE DATA UPLOADED HERE ###
            upload_data = {
                "action": "upload_data",
                "epoch_time": int(time.time() * 1000),
                "data": [
                    {
                        "bed_accelerometer": {
                            "meters_per_second_squared_x": 0,
                            "meters_per_second_squared_y": 0,
                            "meters_per_second_squared_z": 0
                        },
                        "current_position": {
                            "millimeters_x": 0,
                            "millimeters_y": 0,
                            "millimeters_z": 0
                        },
                        "extruder_accelerometer": {
                            "meters_per_second_squared_x": 0,
                            "meters_per_second_squared_y": 0,
                            "meters_per_second_squared_z": 0
                        },
                        "pressure_sensor": {
                            "grams": 50
                        },
                    }
                ]
            }
            ###
            ws.send(json.dumps(upload_data))
            print(c.BLUE + "SENT MESSAGE: " + c.END + str(upload_data))
            time.sleep(5)  # Send a new packet every 5 seconds

    except Exception as e:
        print(c.RED + "ERROR: " + c.END + str(e))
    finally:
        if ws.sock and ws.sock.connected:
            ws.close()
        else:
            print(c.RED + "WEBSOCKET NOT CONNECTED" + c.END)

def check_for_quit():
    global running

    while running:
        user_input = input()
        if user_input.lower() == 'q':
            print(c.RED + "CLOSING CONNECTION" + c.END)
            running = False
            break

if __name__ == "__main__":
    ### 3. CHANGE DEVICE OBJECT HERE ###
    printer = Printer(port="/dev/tty.usbmodem48EF754639541")  # UGA Printer port
    printer.connect()
    ###

    # WebSocket setup
    uri = "wss://stream-digitaltwin.com/machine"
    headers = {
        "x-api-key": os.getenv("APIKEY"),
        "role": "PRIMARY",
        "id": "8hadma98t2"
    }

    ws = websocket.WebSocketApp(uri,
                                header=[f"{key}: {value}" for key, value in headers.items()],
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    # Start a thread to listen for 'q' key press
    threading.Thread(target=check_for_quit, daemon=True).start()

    # WebSocket startup
    try:
        ws.run_forever(sslopt={"context": ssl_context})
    finally:
        # Close the device connection
        printer.close()
