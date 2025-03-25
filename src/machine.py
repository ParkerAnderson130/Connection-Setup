import json
import socket
import time

from abc import ABC, abstractmethod

class Machine(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def set_info(self):
        pass

    @abstractmethod
    def upload_data(self):
        pass

    @abstractmethod
    def send_command(self, command):
        pass