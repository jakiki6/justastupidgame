import threading, datetime, time, sys, os

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
                time.sleep(0.1)
                self.lag = datetime.datetime.now() - self.starttime
                if not threading.main_thread().is_alive():
                    print("Main Thread exited!")
                    sys.exit(0)
            if self.lag > datetime.timedelta(0, 5):
                print("Lag of:", self.lag, end="\r")
            if self.lag > datetime.timedelta(0, 8):
                print("Hang detected!")
                os._exit(1)
            self.tickflag = False
            self.starttime = datetime.datetime.now()
