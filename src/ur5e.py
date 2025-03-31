import ast
import socket
import time
#from rtde_control import RTDEControlInterface

from machine import Machine

class c:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

class UR5e(Machine):
    def __init__(self, host="192.168.1.10", port=30002):
        super().__init__("UR5e Arm")
        self.host = host
        self.port = port
        self.sock = None
        self.vel = 0.5
        self.acc = 0.5
        self.rtde_frequency = 500
        self.ur_cap_port = 50002

    def connect(self):
        print(c.BLUE + f"CONNECTING TO UR5E AT {self.host}:{self.port}" + c.END)
        try:
            
            #rtde_r = RTDEReceive(robot_ip, rtde_frequency)
            #rtde_c = RTDEControl(robot_ip, rtde_frequency, RTDEControl.FLAG_VERBOSE | RTDEControl.FLAG_UPLOAD_SCRIPT, ur_cap_port)
            return c.GREEN + "CONNECTED TO UR5E" + c.END
        except Exception as e:
            return c.RED + f"ERROR CONNECTING TO UR5E: {str(e)}" + c.END
            

    def set_info(self):
        return {
            "action": "set_info",
            "display_name": "UR5e Arm",
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

    def send_command(self, command_str):
        if self.sock:
            try:
                '''
                # Step 1: Extract function name and arguments
                func_name = command_str.split("(")[0]
                args_str = command_str[len(func_name):]
                args = ast.literal_eval(args_str)

                # Step 2: Validate method exists
                if not hasattr(rtde_control, func_name):
                    return c.RED + f"UNKNOWN COMMAND: {func_name}" + c.END

                method = getattr(rtde_control, func_name)

                # Step 3: Call method (wrap in list if needed)
                if not isinstance(args, tuple):
                    args = (args,)
                
                result = method(*args)
                return c.GREEN + f"EXECUTED {func_name} WITH RESULT: {result}" + c.END
                '''
            except Exception as e:
                return c.RED + f"ERROR EXECUTING COMMAND: {str(e)}" + c.END
        else:
            return c.RED + "NOT CONNECTED" + c.END
