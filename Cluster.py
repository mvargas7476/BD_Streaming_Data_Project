"""Cluster.py"""

from datetime import datetime
from math import sqrt, pow
from typing import List

from Point import Point


class Cluster:
    def __init__(self, decay_factor: float = 0.25):
        self._points: List[Point] = []
        self._decay_factor = decay_factor

    def add_point(self, point: Point):
        self._points.append(point)

    def _fade_function(self, current_time: datetime, point_time: datetime) -> float:
        return pow(2, -self._decay_factor * (current_time - point_time).total_seconds() / 60)

    def _cf1(self, current_time: datetime, new_point: Point = None) -> float:
        total = 0
        points = self._points + [new_point] if new_point else self._points
        for point in points:
            total += self._fade_function(current_time, point.timestamp) * point.value
        return total

    def _cf2(self, current_time, new_point: Point = None) -> float:
        total = 0
        points = self._points + [new_point] if new_point else self._points
        for point in points:
            total += self._fade_function(current_time, point.timestamp) * pow(point.value, 2)
        return total

    def weight(self, current_time: datetime, new_point: Point = None) -> float:
        total = 0
        points = self._points + [new_point] if new_point else self._points
        for point in points:
            total += self._fade_function(current_time, point.timestamp)
        return total

    def center(self, current_time: datetime, new_point: Point = None) -> float:
        return self._cf1(current_time, new_point) / self.weight(current_time, new_point)

    def radius(self, current_time: datetime, new_point: Point = None) -> float:
        return sqrt(abs(
            abs(self._cf2(current_time, new_point)) / self.weight(current_time, new_point)
            -
            pow(abs(self._cf1(current_time, new_point)) / self.weight(current_time, new_point), 2)
        ))

    def distance(self, current_time: datetime, point: Point) -> float:
        return abs(self.center(current_time) - point.value)
