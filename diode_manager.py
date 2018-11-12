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

RED_GPIO = 6
GREEN_GPIO = 5
BLUE_GPIO = 11

class DiodeManager:
    def __init__(self, TCP_IP, TCP_PORT):
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.bind(("",TCP_PORT))
        self.server_socket.listen(1)

        self.ir_diodes = [26, 19, 13]
        self.fixation_diode = [9]
        self.rgb_diode = [RED_GPIO, GREEN_GPIO, BLUE_GPIO]
        GPIO.setmode(GPIO.BCM)

        self.create_thread_for_reception()
        self.create_thread_for_displaying()

    def close(self):
        self.server_socket.close()

    def parse_for_configuration_update(self, data):
        results = [int(s) for s in data.split() if s.isdigit()]
        self.fixation_intensity = results[0]
        self.ir_intensity = results[1]
        self.impulse_time = results[2]
        self.impulse_color = results[3]

    def update_configuration(self):
        #ir diodes configuration
        for pwm in self.ir_diodes_pwm:
            pwm.ChangeDutyCycle(self.ir_intensity)
        self.fixation_pwm.ChangeDutyCycle(self.fixation_intensity)
        
        #rgb diode configuration
        if self.impulse_color == 1:
            color = RED_GPIO
        elif self.impulse_color == 2:
            color = GREEN_GPIO
        else:
            color = BLUE_GPIO

        GPIO.output(color, 0)
        sleep(self.impulse_time)
        GPIO.output(color, 1)


    def receive(self):
        print("Started listening")
        sleep(1)
        while(SHOULD_THREAD_RUN):
            self.connection, address = self.server_socket.accept()
            data = self.connection.recv(BUFFER_SIZE).decode()
            print("Received: ", data)
            if((data != "QUIT")or(data != " ")):
                self.parse_for_configuration_update(data)
                self.update_configuration()

        self.connection.close()
        print("Destroyed reception thread!")

    def display(self):
            #ir diodes configuration
            self.ir_diodes_pwm = []
            for diode in self.ir_diodes:
                GPIO.setup(diode, GPIO.OUT, initial = GPIO.HIGH)
                self.ir_diodes_pwm.append(GPIO.PWM(diode, 50))
            for pwm in self.ir_diodes_pwm:
                pwm.start(20)

            # fixation diode conifguration
            GPIO.setup(self.fixation_diode[0], GPIO.OUT, initial = GPIO.HIGH)
            self.fixation_pwm = GPIO.PWM(self.fixation_diode[0],50)
            self.fixation_pwm.start(100)

            #rgb diode configuration
            for rgb_wire in self.rgb_diode:
                GPIO.setup(rgb_wire, GPIO.OUT, initial = GPIO.HIGH)

            while(SHOULD_THREAD_RUN):
                continue
    
            print("Destroyed display thread!")
            for pwm in self.ir_diodes_pwm:
                pwm.stop()
            self.fixation_pwm.stop()
            for rgb_wire in self.rgb_diode:
                GPIO.setup(rgb_wire, GPIO.OUT, initial = GPIO.HIGH)

            GPIO.cleanup()

            
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


