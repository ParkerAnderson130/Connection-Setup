import json
import os
import random
import time
import threading
import websocket
from dotenv import load_dotenv
load_dotenv()
from printer import Printer

websocket.enableTrace(False)

def on_message(ws, message):
    print(f"Received response: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")

def on_open(ws):
    print("Connected to WebSocket server")
    threading.Timer(0.5, send_single_message, args=(ws,)).start()

def send_single_message(ws):
    # Define message data
    data = {
        "action": "set_info",
        "machine_type": "3D_PRINTER",
        "display_name": "UGA Printer",
        "commands": {
            "Test": {
                "description": "Test to see if this command renders",
                "usage": "test <TEST>"
            }
        },
        "sensors": {
            "temperature_one": {
                "display_name": "Main Temperature Sensor",
                "sensor_type": "TEMPERATURE",
                "metrics": {
                    "degrees_celsius": {
                        "display_name": "°C",
                        "byte_count": 2
                    }
                }
            },
        }
    }

    '''
    data = {
        "action": "upload_data",
        "epoch_time": int(time.time()),
        "data": {
            "temperature_one": {
                "degrees_celsius": random.randint(30, 60)
            },
        }
    }
    '''
    
    try:
        # Check if the WebSocket is open before sending
        if ws.sock and ws.sock.connected:
            ws.send(json.dumps(data))
            print(f"Sent message: {data}")
        else:
            print("WebSocket not connected.")
    except Exception as e:
        print(f"Error sending message: {e}")
    finally:
        time.sleep(5) # Wait to observe any server response before closing
        if ws.sock and ws.sock.connected:
            ws.close()
        else:
            print("WebSocket already closed or disconnected.")

if __name__ == "__main__":
    uri = "wss://stream-digitaltwin.com/machine" #"ws://0.0.0.0:8081/machine"
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
    ws.run_forever()