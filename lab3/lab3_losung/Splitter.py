import zmq
import threading
import time
from time import sleep

import constPipe as const

class Splitter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def initWordCount(self, text):
        self.text = text
        print("Der Herr der Ringe - Die Gefährten Kapitel 1 erhalten.")

    def run(self):
        context = zmq.Context()

        mapperSocket = context.socket(zmq.PUSH)
        mapperSocket.bind(f"tcp://*:{const.PORT1}")
        lines = str.splitlines(self.text)

        sleep(2)

        for line in lines:
            mapperSocket.send_string(f"{line}")
