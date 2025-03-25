import certifi
from collections import deque
import datetime
import dotenv
from dotenv import load_dotenv
import json
import os
import time
import threading
import ssl
import websocket

from ur5e import UR5e

class c:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

load_dotenv()
ssl_context = ssl.create_default_context(cafile=certifi.where())

running = True
latency_tracker = deque()
LATENCY_LOG_FILE = "latency_log.txt"
data = []

def on_message(ws, message):
    print(c.BLUE + "MESSAGE: " + c.END + message)
    try:
        data = json.loads(message)

        if "status_code" in data and data["status_code"] == 200:
            log_latency(latency_tracker[0][0], latency_tracker[0][1])
            latency_tracker.popleft()

        if data.get("action") == "send_command":
            command = data.get("command")
            if command:
                print(c.GREEN + "EXECUTING COMMAND: " + c.END + command)
                response = machine.send_command(command)
                print(c.BLUE + "RESPONSE: " + c.END + response)
            else:
                print(c.RED + "ERROR: No 'command' field found in the message." + c.END)

    except Exception as e:
        print(c.RED + f"ERROR: {str(e)}" + c.END)

def on_error(ws, error):
    print(c.RED + "ERROR: " + c.END + str(error))

def on_close(ws, close_status_code, close_msg):
    print(c.RED + "CLOSED: " + c.END + f"{close_status_code}, message: {close_msg}")

def on_open(ws):
    print(c.GREEN + "CONNECTED" + c.END)
    threading.Thread(target=send_multiple_messages, args=(ws,)).start()

def send_multiple_messages(ws):
    global running
    try:
        if ws.sock and ws.sock.connected:
            ws.send(json.dumps(machine.set_info()))
            latency_tracker.append(["set_info", time.time()])
            print(c.GREEN + "SENT MESSAGE: " + c.END + str(machine.set_info()))
        else:
            print(c.RED + "WEBSOCKET NOT CONNECTED" + c.END)

        while running and ws.sock and ws.sock.connected:
            ws.send(json.dumps(machine.upload_data()))
            latency_tracker.append(["upload_data", time.time()])
            print(c.BLUE + "SENT MESSAGE: " + c.END + str(machine.upload_data()))
            time.sleep(5)

    except Exception as e:
        print(c.RED + "ERROR: " + c.END + str(e))
    finally:
        if ws.sock and ws.sock.connected:
            ws.close()
        else:
            print(c.RED + "WEBSOCKET NOT CONNECTED" + c.END)

def log_latency(action, start_time):
    latency = time.time() - start_time
    data.append(latency)
    with open(LATENCY_LOG_FILE, "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} | Action: {action} | Latency: {latency:.4f} seconds\n")
    print(c.GREEN + f"LOGGED LATENCY: {latency:.4f} seconds for Action: {action}" + c.END)

if __name__ == "__main__":
    machine = UR5e(host="192.168.1.10")
    machine.connect()

    uri = "wss://stream-digitaltwin.com/machine"
    #uri = "ws://0.0.0.0:8081/machine"
    headers = {
        "x-api-key": os.getenv("APIKEY"),
        "role": "PRIMARY",
        "id": "gbfy3v84x5"
    }

    ws = websocket.WebSocketApp(uri,
                                header=[f"{key}: {value}" for key, value in headers.items()],
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    threading.Thread(target=send_multiple_messages, args=(ws,)).start()
    ws.run_forever(sslopt={"context": ssl_context})
