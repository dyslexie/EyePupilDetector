import sys
sys.path.append("../")
import socket
import _thread
from time import sleep
import RPi.GPIO as GPIO


import signal
import sys

SHOULD_THREAD_RUN = True
BUFFER_SIZE = 1024

class DiodeManager:
    def __init__(self, TCP_IP, TCP_PORT):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind(("",TCP_PORT))
        self.server_socket.listen(1)
        self.intensity = 1

        self.__diodes = [26,19,13,6,5,11]
        self.__indicators = [9,10]
        GPIO.setmode(GPIO.BCM)

        self.create_thread_for_reception()
        self.create_thread_for_displaying()

    def close(self):
        self.server_socket.close()

    def parse_for_freq_and_intensity(self, data):
        results = [int(s) for s in data.split() if s.isdigit()]
        self.intensity = results[0]

    def receive(self):
        print("Started listening")
        sleep(1)
        while(SHOULD_THREAD_RUN):
            self.connection, address = self.server_socket.accept()
            data = self.connection.recv(BUFFER_SIZE).decode()
            print("Received: ", data)
            if((data != "QUIT")or(data != " ")):
                self.parse_for_freq_and_intensity(data)
                for diode in self.diode_list:
                    diode.ChangeDutyCycle(self.intensity)


        self.connection.close()
        print("Destroyed reception thread!")

    def display(self):
            self.diode_list = []
            for diode in self.__diodes:
                GPIO.setup(diode, GPIO.OUT, initial = GPIO.HIGH)
                self.diode_list.append(GPIO.PWM(diode, 50))

            for pwm in self.diode_list:
                pwm.start(self.intensity)

            while(SHOULD_THREAD_RUN):
                continue
    
            print("Destroyed display thread!")
            for pwm in self.diode_list:
                pwm.stop()
            
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
        sleep(2)
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

manager = DiodeManager("", 2222)

while True:
    continue


