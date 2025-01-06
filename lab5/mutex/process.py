import logging
import random
import time
from datetime import datetime

from constMutex import ENTER, RELEASE, ALLOW, ACTIVE

class Process:
    def __init__(self, chan):
        self.channel = chan
        self.process_id = self.channel.join('proc')
        self.all_processes = []
        self.other_processes = []
        self.queue = []
        self.clock = 0
        self.peer_name = 'unassigned'
        self.peer_type = 'unassigned'
        self.logger = logging.getLogger("vs2lab.lab5.mutex.process.Process")
        self.last_seen = {}  # Zuletzt gesehene Zeitstempel pro Prozess
        self.timeout_limit = 10  # Timeout in Sekunden, um Prozess als ausgefallen zu betrachten

    def __mapid(self, id='-1'):
        if id == '-1':
            id = self.process_id
        return 'Proc-' + str(id)

    def __cleanup_queue(self):
        if len(self.queue) > 0:
            self.queue.sort()
            while len(self.queue) > 0 and self.queue[0][2] == ALLOW:
                del self.queue[0]

    def __request_to_enter(self):
        self.clock += 1
        request_msg = (self.clock, self.process_id, ENTER)
        self.queue.append(request_msg)
        self.__cleanup_queue()
        self.channel.send_to(self.other_processes, request_msg)

    def __allow_to_enter(self, requester):
        self.clock += 1
        msg = (self.clock, self.process_id, ALLOW)
        self.channel.send_to([requester], msg)

    def __release(self):
        assert self.queue[0][1] == self.process_id, 'State error: inconsistent local RELEASE'
        self.queue = [r for r in self.queue[1:] if r[2] == ENTER]
        self.clock += 1
        msg = (self.clock, self.process_id, RELEASE)
        self.channel.send_to(self.other_processes, msg)

    def __allowed_to_enter(self):
        processes_with_later_message = set([req[1] for req in self.queue[1:]])
        first_in_queue = self.queue[0][1] == self.process_id
        all_have_answered = len(self.other_processes) == len(processes_with_later_message)
        return first_in_queue and all_have_answered

    def __receive(self):
        _receive = self.channel.receive_from(self.other_processes, 3)
        current_time = datetime.now()

        if _receive:
            msg = _receive[1]
            sender = msg[1]
            self.last_seen[sender] = current_time  # Aktualisiere Zeitstempel

            self.clock = max(self.clock, msg[0]) + 1
            self.logger.debug("{} received {} from {}.".format(
                self.__mapid(),
                "ENTER" if msg[2] == ENTER else "ALLOW" if msg[2] == ALLOW else "RELEASE",
                self.__mapid(sender)
            ))

            if msg[2] == ENTER:
                self.queue.append(msg)
                self.__allow_to_enter(sender)
            elif msg[2] == ALLOW:
                self.queue.append(msg)
            elif msg[2] == RELEASE:
                assert self.queue[0][1] == sender and self.queue[0][2] == ENTER, \
                    'State error: inconsistent remote RELEASE'
                del self.queue[0]

            self.__cleanup_queue()
        else:
            self.logger.info("{} timed out on RECEIVE. Local queue: {}".
                             format(self.__mapid(),
                                    list(map(lambda msg: (
                                        'Clock ' + str(msg[0]),
                                        self.__mapid(msg[1]),
                                        msg[2]), self.queue))))

        self.__check_for_failures()

    def __check_for_failures(self):
        """Prüfe, ob andere Prozesse als ausgefallen betrachtet werden sollten."""
        current_time = datetime.now()
        for proc in self.other_processes[:]:
            if proc not in self.last_seen:
                self.last_seen[proc] = current_time  # Initialer Zeitstempel
            elif (current_time - self.last_seen[proc]).total_seconds() > self.timeout_limit:
                self.logger.warning(f"Process {self.__mapid(proc)} is considered crashed.")
                self.other_processes.remove(proc)  # Entferne den ausgefallenen Prozess
                self.all_processes.remove(proc)  # Entferne aus der Gesamtübersicht

    def init(self, peer_name, peer_type):
        self.channel.bind(self.process_id)
        self.all_processes = list(self.channel.subgroup('proc'))
        self.all_processes.sort(key=lambda x: int(x))
        self.other_processes = list(self.channel.subgroup('proc'))
        self.other_processes.remove(self.process_id)
        self.peer_name = peer_name
        self.peer_type = peer_type
        self.logger.info("{} joined channel as {}.".format(
            peer_name, self.__mapid()))

    def run(self):
        while True:
            if len(self.all_processes) > 1 and \
                    self.peer_type == ACTIVE and \
                    random.choice([True, False]):
                self.logger.debug("{} wants to ENTER CS at CLOCK {}."
                                  .format(self.__mapid(), self.clock))

                self.__request_to_enter()
                while not self.__allowed_to_enter():
                    self.__receive()

                sleep_time = random.randint(0, 2000)
                self.logger.debug("{} enters CS for {} milliseconds."
                                  .format(self.__mapid(), sleep_time))
                print(" CS <- {}".format(self.__mapid()))
                time.sleep(sleep_time / 1000)
                print(" CS -> {}".format(self.__mapid()))
                self.__release()
                continue

            if random.choice([True, False]):
                self.__receive()
