import serial
import time

def test_3d_printer_connection(port, baudrate=115200, timeout=2):
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as printer:
            print(f"Connected to {port} at {baudrate} baud.")
        
            time.sleep(2)
            
            gcode_command = "M105\n"  # Requests the current temperature
            printer.write(gcode_command.encode())
            print(f"Sent: {gcode_command.strip()}")

            response = printer.readline().decode().strip()
            print(f"Received: {response}")

    except serial.SerialException as e:
        print(f"Serial exception: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    port = "/dev/ttyUSB0"  # Replace with printer's port on Raspberry Pi
    test_3d_printer_connection(port)