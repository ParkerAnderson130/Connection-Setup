import serial
import time

port = '/dev/tty.usbmodem48EF754639541'
baud_rate = 115200

with serial.Serial(port, baud_rate, timeout=1) as ser:
    time.sleep(2)

    # Send a G-code command (e.g., get temp)
    ser.write(b"G28\n")
    time.sleep(0.5)

    while ser.in_waiting > 0:
        response = ser.readline().decode().strip()
        print("Response:", response)
