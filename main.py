# main.py

import json
import os
import time
import threading
import websocket
from dotenv import load_dotenv
load_dotenv()
from printer import Printer

# WebSocket functions
def on_message(ws, message):
    print(f"Received response: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")

def on_open(ws, initial=True):
    print("Connected to WebSocket server")
    threading.Timer(0.5, send_single_message, args=(ws, initial)).start()

def send_single_message(ws, initial):
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

    update_data = {
        "action": "upload_data",
        "epoch_time": int(time.time()),
        "data": {
            "temperature_one": {
                "degrees_celsius": printer.getTemperature()
            }
        }
    }

    try:
        if ws.sock and ws.sock.connected:
            if initial:
                ws.send(json.dumps(set_info))
                print(f"Sent message: {set_info}")
            else:
                ws.send(json.dumps(update_data))
                print(f"Sent message: {update_data}")
        else:
            print("WebSocket not connected.")
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        time.sleep(5)
        if ws.sock and ws.sock.connected:
            ws.close()
        else:
            print("WebSocket already closed or disconnected.")

if __name__ == "__main__":
    # Printer setup
    printer = Printer(port="/dev/ttyUSB0") # Replace with the actual port for the 3D printer
    printer.connect()

    # WebSocket setup
    uri = "wss://stream-digitaltwin.com/machine"
    headers = {
        "x-api-key": os.getenv("APIKEY"),
        "role": "PRIMARY",
        "id": "8hadma98t2"
    }

    ws = websocket.WebSocketApp(uri,
                                header=[f"{key}: {value}" for key, value in headers.items()],
                                on_open=lambda ws: on_open(ws, initial=True), # Pass initial
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    # Run the WebSocket connection
    ws.run_forever()
    
    # Clean up printer connection on exit
    printer.close()
