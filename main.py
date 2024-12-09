#main.py

import json
import os
import time
import threading
import certifi
from dotenv import load_dotenv
import ssl
import websocket

from printer import Printer

load_dotenv()
ssl_context = ssl.create_default_context(cafile=certifi.where())

# WebSocket functions
def on_message(ws, message):
    print(f"Received response: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")

def on_open(ws):
    print("Connected to WebSocket server")
    threading.Thread(target=send_multiple_messages, args=(ws,)).start()

def send_multiple_messages(ws):
    ### 1. CHANGE DEVICE SPECIFIC INFORMATION HERE ###
    set_info = {
        "action": "set_info",
        "display_name": "UGA Printer",
        "machine_type": "3D_PRINTER",
        "gcode": True,
        "sensors": {
            "temperature_one": {
                "display_name": "Primary Temperature Sensor",
                "sensor_type": "TEMPERATURE",
                "metrics": {
                    "degrees_celsius": {
                        "display_name": "°C",
                        "byte_count": 2
                    }
                }
            }
        }
    }
    ###

    try:
        # Send the initial "set_info" packet
        if ws.sock and ws.sock.connected:
            ws.send(json.dumps(set_info))
            print(f"Sent message: {set_info}")
        else:
            print("WebSocket not connected.")

        # Send "upload_data" packets to update STREAM
        while ws.sock and ws.sock.connected:
            ### 2. CHANGE DATA UPLOADED HERE ###
            update_data = {
                "action": "upload_data",
                "epoch_time": int(time.time()),
                "data": {
                    "temperature_one": {
                        "degrees_celsius": printer.getTemperature()
                    }
                }
            }
            ###
            ws.send(json.dumps(update_data))
            print(f"Sent message: {update_data}")
            time.sleep(5) # Send a new packet every 5 seconds

    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        if ws.sock and ws.sock.connected:
            ws.close()
        else:
            print("WebSocket already closed or disconnected.")

if __name__ == "__main__":
    ### 3. CHANGE DEVICE OBJECT HERE ###
    printer = Printer(port="/dev/tty.usbmodem48EF754639541") # UGA Printer port
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
    
    # Run the WebSocket connection
    ws.run_forever(sslopt={"context": ssl_context})
    
    # Close Printer connection 
    printer.close()
