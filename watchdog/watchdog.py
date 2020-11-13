import threading, datetime, time, sys, os, gc

class Watchdog(threading.Thread):
    def __init__(self, threads):
        super().__init__()
        self.threads = threads
    def run(self):
        while True:
            for thread in self.threads:
                if not thread.is_alive():
                    print(f"{thread.name} died!")
                    os._exit(1)
            time.sleep(0.5)
