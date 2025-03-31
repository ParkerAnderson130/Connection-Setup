import socket
import time

# Replace with your UR5e IP (update this after finding the correct IP)
UR5E_IP = "192.168.1.100"  # Update this with the actual IP
UR5E_PORT = 30002  # Secondary program port for URScript commands

# URScript command to move only the base joint (first joint) slowly
ur_script = """
def test_single_joint():
    # Get current joint positions
    current_pos = get_actual_joint_positions()
    
    # Create new target position (only changing base joint)
    target_pos = [0.5, current_pos[1], current_pos[2], 
                 current_pos[3], current_pos[4], current_pos[5]]
    
    # Move to target position slowly
    # a=0.5 (low acceleration), v=0.1 (low velocity)
    movej(target_pos, a=0.5, v=0.1)
end
"""

def send_ur_command(command: str, ip: str, port: int):
    """Send a URScript command to the UR5e arm via TCP socket."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)  # Timeout in seconds
            s.connect((ip, port))  # Connect to UR5e
            s.sendall(command.encode('utf-8'))  # Send command
            print("Command sent to UR5e successfully.")

            # Increased sleep time for slower movement
            time.sleep(3)  # Wait for movement to complete

    except socket.error as e:
        print(f"Socket error: {e}")

if __name__ == "__main__":
    print(f"Attempting to connect to UR5E at {UR5E_IP}:{UR5E_PORT}")
    send_ur_command(ur_script, UR5E_IP, UR5E_PORT)