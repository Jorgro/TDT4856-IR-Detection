from dataclasses import dataclass
import random
from typing import List
import cv2

@dataclass
class Point:
    x: int
    y: int


def get_area(p1: Point, p2: Point) -> int:
    return (p2.x - p1.x) * (p2.y - p2.y)

