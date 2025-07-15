import time

class Timer:
    def __init__(self):
        self._timers = {}

    def start(self, key: str) -> None:
        self._timers[key] = time.time()

    def stop(self, key: str) -> None:
        if key in self._timers:
            self._timers[key] = time.time() - self._timers[key]

    def get_duration(self, key: str) -> float:
        return self._timers.get(key, -1.0)
