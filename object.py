from typing import List
import cv2
import numpy as np
from utils import Point


class Object:
    UID = 1

    def __init__(
        self, x: int, y: int, w: int, h: int, area: float, center: np.array,
    ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = area
        self.center = center
        self.positions: List[np.array] = [self.center]
        self.updated = True
        self.unique_id = Object.UID
        Object.UID += 1

    def get_bbx(self) -> List[Point]:
        return [Point(self.x, self.y), Point(self.x + self.w, self.y + self.h)]

    def update(self, x, y, w, h, area, center):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = area
        self.center = center
        self.updated = True
        self.positions.append(self.center)

    def __hash__(self):
        return str(self.unique_id)

    def __repr__(self):
        return f"Object({self.center[0]},{self.center[1]})"
