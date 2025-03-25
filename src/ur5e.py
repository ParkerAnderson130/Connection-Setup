import socket
import time

from machine import Machine

class c:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

class UR5e(Machine):
    def __init__(self, host="192.168.1.10", port=30002):
        super().__init__("Dummy Robot Arm")
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        print(c.BLUE + f"CONNECTING TO UR5E AT {self.host}:{self.port}" + c.END)
        '''
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=10)
            print(c.GREEN + f"CONNECTED TO UR5E" + c.END)
        except Exception as e:
            print(c.RED + f"ERROR CONNECTING TO UR5E: {e}" + c.END)
        '''

    def set_info(self):
        return {
            "action": "set_info",
            "display_name": "UR5e Robotic Arm",
            "machine_type": "ROBOTIC_ARM",
            "sensors": {
                "tcp_position": {
                    "display_name": "TCP Position",
                    "sensor_type": "POSITION",
                    "metrics": {
                        "x": {
                            "display_name": "X Position (m)",
                            "byte_count": 4
                        },
                        "y": {
                            "display_name": "Y Position (m)",
                            "byte_count": 4
                        },
                        "z": {
                            "display_name": "Z Position (m)",
                            "byte_count": 4
                        }
                    }
                },
                "joint_angles": {
                    "display_name": "Joint Angles",
                    "sensor_type": "ANGLE",
                    "metrics": {
                        "j1": {
                            "display_name": "Joint 1 Angle (Shoulder)",
                            "byte_count": 4
                        },
                        "j2": {
                            "display_name": "Joint 2 Angle (Upper Arm)",
                            "byte_count": 4
                        },
                        "j3": {
                            "display_name": "Joint 3 Angle (Elbow)",
                            "byte_count": 4
                        },
                        "j4": {
                            "display_name": "Joint 4 Angle (Wrist 1)",
                            "byte_count": 4
                        },
                        "j5": {
                            "display_name": "Joint 5 Angle (Wrist 2)",
                            "byte_count": 4
                        },
                        "j6": {
                            "display_name": "Joint 6 Angle (Wrist 3)",
                            "byte_count": 4
                        }
                    }
                }
            }
        }

    def upload_data(self):
        return {
            "action": "upload_data",
            "epoch_time": int(time.time() * 1000),
            "data": {
                "tcp_position": {
                    "x": 0.482,
                    "y": 0.120,
                    "z": 0.325
                },
                "joint_angles": {
                    "j1": 0.15,
                    "j2": -1.45,
                    "j3": 0.65,
                    "j4": -0.75,
                    "j5": 1.25,
                    "j6": -0.35
                }
            }
        }

    def send_command(self, command):
        if self.sock:
            try:
                self.sock.sendall(command.encode() + b"\n")
                time.sleep(0.1)
                return "Command sent successfully"
            except Exception as e:
                return e
        else:
            return "Not connected"