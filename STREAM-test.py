import websocket
import json

def on_message(ws, message):
    print(f"Received response: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def on_open(ws):
    print("Connected to WebSocket server")
    
    # Send initial payload
    data = {
        "action": "upload_data",
        "epoch_time": 0,
        "data": {
            "temperature_one": {"degrees_celsius": 30},
            "temperature_two": {"degrees_celsius": 32}
        }
    }
    ws.send(json.dumps(data))
    print(f"Sent message: {data}")

if __name__ == "__main__":
    websocket.enableTrace(True)
    
    uri = "ws://0.0.0.0:8080/machine"
    headers = {
        "x-api-key": "sUjpcMXAJM84OTcIcS9tn7czv7Ew4X8C9QCEUeKw",
        "role": "PRIMARY",
        "id": "8hadma98t2"
    }
    
    # Create a WebSocket connection with headers
    ws = websocket.WebSocketApp(uri,
                                header=[f"x-api-key: {headers['x-api-key']}",
                                        f"role: {headers['role']}",
                                        f"id: {headers['id']}"],
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    # Run the WebSocket
    ws.run_forever()