import sys
sys.path.append("../")
import socket
import _thread
from time import sleep

import signal
import sys

SHOULD_THREAD_RUN = True
BUFFER_SIZE = 1024

class DiodeManager:
    def __init__(self, TCP_IP, TCP_PORT):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind((TCP_IP,TCP_PORT))
        self.server_socket.listen(1)
        self.intensity = 0
        self.frequency = 0

        self.create_thread_for_reception()
        self.create_thread_for_displaying()

    def close(self):
        self.server_socket.close()

    def parse_for_freq_and_intensity(self, data):
        results = [int(s) for s in data.split() if s.isdigit()]
        self.frequency = results[0]
        self.intensity = results[1]

    def receive(self):
        print("Started listening")
        sleep(1)
        while(SHOULD_THREAD_RUN):
            self.connection, address = self.server_socket.accept()
            data = self.connection.recv(BUFFER_SIZE).decode()
            print("SERVER_LOG (received): ", data)
            if(data != "QUIT"):
                self.parse_for_freq_and_intensity(data)


        self.connection.close()
        print("Destroyed reception thread!")

    def display(self):
        while(SHOULD_THREAD_RUN):
            print("VALUES: ", str(self.frequency), str(self.intensity), str(SHOULD_THREAD_RUN))
            sleep(0.1)
        print("Destroyed display thread!")

    def create_thread_for_reception(self):
        print("Started thread for reception")
        _thread.start_new_thread(self.receive,())

    def create_thread_for_displaying(self):
        print("Started thread for display")
        _thread.start_new_thread(self.display,())

def signal_handler(sig, frame):
        print('You pressed Ctrl+C! - switching to false')
        global SHOULD_THREAD_RUN
        SHOULD_THREAD_RUN = False
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(('localhost',2222))
        client.send("QUIT".encode())
        client.close()
        sleep(2)
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

manager = DiodeManager('localhost', 2222)


while True:
    continue

# i = 0
# while True:
#     i = i + 1
#     client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     client.connect(('localhost',2222))
#     client.send(("UPDATE_CONF: " + str(i) + " " +str(i+1)).encode())
#     client.close()
#     sleep(1)

