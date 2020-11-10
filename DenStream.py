from typing import List
from datetime import datetime

from Point import Point
from Cluster import Cluster


class DenStream:
    def __init__(self):
        self.cp_memory: List[Cluster] = []
        self.co_memory: List[Cluster] = []

        self.max_radius = 0.3  # epsilon
        self.min_weight = 10  # mu
        self.decay_factor = 0.25  # lambda
        self.outlier_threshold = 0.15  # beta

    @staticmethod
    def nearest_cluster_index(current_time: datetime, clusters: List[Cluster], point: Point) -> int:
        if not clusters:
            return -1
        distances = [cluster.distance(current_time, point) for cluster in clusters]
        return distances.index(min(distances))

    def new_co(self, initial_point: Point):
        new_co = Cluster(self.decay_factor)
        new_co.add_point(initial_point)
        self.co_memory.append(new_co)

    # Returns true if DenStream thinks it is not an outlier
    def merge(self, current_time: datetime, new_point: Point) -> bool:
        nearest_cp = DenStream.nearest_cluster_index(current_time, self.cp_memory, new_point)
        if nearest_cp > -1 and self.cp_memory[nearest_cp].radius(current_time, new_point) <= self.max_radius:
            self.cp_memory[nearest_cp].add_point(new_point)
            return True
        else:
            nearest_co = DenStream.nearest_cluster_index(current_time, self.co_memory, new_point)
            if nearest_co > -1 and self.co_memory[nearest_co].radius(current_time, new_point) <= self.max_radius:
                self.co_memory[nearest_co].add_point(new_point)
                weight = self.co_memory[nearest_co].weight(current_time)
                beta_mu = self.min_weight * self.outlier_threshold
                if weight > beta_mu:
                    self.cp_memory.append(self.co_memory[nearest_co])
                    self.co_memory.pop(nearest_co)
                    return True
            else:
                self.new_co(new_point)

        return False
