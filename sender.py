import _thread
import socket
import threading
import time

import timer

SENDER_ADDRESS = ('localhost', 6663)
SLEEP_INTERVAL = 0.05

last_ack_received = -1
timer_object = timer.Timer() # instanta a clasei timer

class Sender(threading.Thread):

    def __init__(self, filename, PACKET_SIZE, WINDOW_SIZE, LOSS_CHANCE, CORRUPTION_CHANCE, TIMEOUT):
        super().__init__()
        self.running = True

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(SENDER_ADDRESS)
        self.filename = filename

        self.PACKET_SIZE = PACKET_SIZE
        self.WINDOW_SIZE = WINDOW_SIZE
        self.LOSS_CHANCE = LOSS_CHANCE
        self.CORRUPTION_CHANCE = CORRUPTION_CHANCE
        self.TIMEOUT = TIMEOUT

    def run(self):
        global last_ack_received
        global timer_object

        print('Sender has started.')

        try:
            file = open(self.filename, 'rb') # format binar
        except IOError:
            running = False;
            return
        # cream vectorul packet si adaugam in buffer
        packets = []
        packet_number = 0

        while True:
            data = file.read(self.PACKET_SIZE)
            if not data:
                break
            # adaugam pachetele in vectorul packets TODO

        number_of_packets = len(packets)
        window_size = min(self.WINDOW_SIZE, number_of_packets)

        last_frame_sent = -1

        # rulam pana cand toate pachetele sunt trimise
        while self.running and last_ack_received < number_of_packets - 1:
            # start timer
            if not timer_object.timer_is_running():
                timer_object.start()

            # trimitem pachetele din fereastra
            while last_frame_sent < last_ack_received + window_size:
                last_frame_sent += 1

            # thread -> sleep pana cand avem un timeout sau ack
            while timer_object.timer_is_running() and not timer_object.timeout():
                time.sleep(SLEEP_INTERVAL)

            if timer_object.timeout():
                timer_object.stop()
                last_frame_sent = last_ack_received
            else:
                # daca nu avem timeout inseamna ca avem confirmarea corecta
                window_size = min(self.WINDOW_SIZE, number_of_packets - last_ack_received - 1)

        if last_ack_received > number_of_packets:
            self.socket.close()


        if self.running:
            self.socket.close()
        else:
            self.socket.close()


    def terminate(self):
        self.running = False


def run_sender(filename, PACKET_SIZE, WINDOW_SIZE, LOSS_CHANCE, CORRUPTION_CHANCE, TIMEOUT):
    sender = Sender(filename, PACKET_SIZE, WINDOW_SIZE, LOSS_CHANCE, CORRUPTION_CHANCE, TIMEOUT)
    sender.run()


if __name__ == '__main__':
    filename = f"test send test.jpg"
    PACKET_SIZE = 4096
    WINDOW_SIZE = 32
    LOSS_CHANCE = 5
    CORRUPTION_CHANCE = 1
    TIMEOUT = 0.5

    run_sender(filename, PACKET_SIZE, WINDOW_SIZE, LOSS_CHANCE, CORRUPTION_CHANCE, TIMEOUT)