from datetime import datetime


class Point:
    def __init__(self, timestamp: datetime, value: float):
        self._timestamp = timestamp
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def timestamp(self):
        return self._timestamp

    def __sub__(self, other):
        return self._value - other.value

    def __str__(self):
        return str(self._timestamp) + "," + str(self._value)
