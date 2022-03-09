import random
import numpy as np
from typing import Dict, List, Tuple
from object import Object
from utils import Point
import cv2


class ClassifiedObject(Object):
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
        super().__init__(x, y, w, h, area, center)
        self.classification = classification

    def __repr__(self):
        return f"ClassifiedObject({self.center[0]},{self.center[1]})"

def get_image_with_bbx(class_objs: List[Object], image):
    output = np.copy(image)
    for obj in class_objs:
        bbx = obj.get_bbx()
        # Plots one bounding box on image img
        tl = (
            round(0.002 * (output.shape[0] + output.shape[1]) / 2) + 1
        )  # line thickness
        c1, c2 = (bbx[0].x, bbx[0].y), (bbx[1].x, bbx[1].y)
        cv2.rectangle(output, c1, c2, (0, 255, 0), thickness=tl)

        if isinstance(obj, ClassifiedObject) and obj.classification:
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