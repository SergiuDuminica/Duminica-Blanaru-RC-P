import time

class Timer(object):
    TIMER_STOP = -1

    def __init__(self, duration):
        self._start_time = self.TIMER_STOP
        self._duration = duration

    def start(self):
        if self._start_time == self.TIMER_STOP:
            self._start_time = time.time()

    def stop(self):
        if self._start_time != self.TIMER_STOP:
            self._start_time = self.TIMER_STOP

    def running(self):
        return self._start_time != self.TIMER_STOP

    def timeout(self):
        if not self.running():
            return False
        else:
            return time.time() - self._start_time >= float(self._duration)
