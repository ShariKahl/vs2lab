import zmq
import threading
from collections import defaultdict

import constPipe as const

class Reducer(threading.Thread):
    def __init__(self, port):
        self.port = port
        self.words = defaultdict(int)
        threading.Thread.__init__(self)

    def run(self):
        context = zmq.Context()

        mapperSocket = context.socket(zmq.PULL)
        mapperSocket.bind(f"tcp://localhost:{self.port}")

        while True:
            word = mapperSocket.recv().decode('UTF-8')
            self.words[word] += 1

            print(f"Das Wort: '{word}' wurde empfangen und zwar ganze {self.words[word]} mal.")

