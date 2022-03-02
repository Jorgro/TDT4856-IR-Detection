import random
import numpy as np
from typing import Dict, List, Tuple
from utils import Point
import cv2


class ClassifiedObject:
    UID = 1

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        area: float,
        center: np.array,
        conf: float,
        classification: str,
    ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = area
        self.center = center
        self.conf = conf
        self.classification = classification
        self.positions: List[np.array] = [self.center]
        self.updated = True
        self.unique_id = ClassifiedObject.UID
        ClassifiedObject.UID += 1

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
        return f"ClassifiedObject({self.center[0]},{self.center[1]})"


def get_image_with_bbx(class_objs: List[ClassifiedObject], image):
    output = np.copy(image)
    for obj in class_objs:
        bbx = obj.get_bbx()
        # Plots one bounding box on image img
        tl = (
            round(0.002 * (output.shape[0] + output.shape[1]) / 2) + 1
        )  # line thickness
        c1, c2 = (bbx[0].x, bbx[0].y), (bbx[1].x, bbx[1].y)
        cv2.rectangle(output, c1, c2, (0, 255, 0), thickness=tl)
        if obj.classification:
            tf = max(tl - 1, 1)  # font thickness
            t_size = cv2.getTextSize(
                obj.classification, 0, fontScale=tl / 3, thickness=tf
            )[0]
            c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
            cv2.rectangle(output, c1, c2, (0, 255, 0), -1)  # filled
            cv2.putText(
                output,
                obj.classification,
                (c1[0], c1[1] - 2),
                0,
                tl / 3,
                [0, 0, 0],
                thickness=tf,
                lineType=cv2.LINE_AA,
            )
    return output
