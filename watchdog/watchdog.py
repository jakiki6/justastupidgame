import threading, datetime, time

class Watchdog(threading.Thread):
    def __init__(self):
        super().__init__()
        self.tickflag = False
        self.starttime = datetime.datetime.now()
        self.lag = datetime.datetime.now() - datetime.datetime.now()
    def tick(self):
        self.tickflag = True
    def run(self):
        while True:
            while not self.tickflag:
                time.sleep(0.01)
            self.tickflag = False
            self.lag = datetime.datetime.now() - self.starttime
            self.starttime = datetime.datetime.now()
