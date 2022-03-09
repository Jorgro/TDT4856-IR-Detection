from typing import List
from moving_object_detection.moving_object_detector import MovingObject
from object_classifier.classified_object import ClassifiedObject
from utils import get_area


class ObjectMerger:
    def merge_objects(
        self,
        moving_objects: List[MovingObject],
        classified_objects: List[ClassifiedObject],
    ):
        self.moving_classified_objects: List[ClassifiedObject] = []

        for mov_obj in moving_objects:

            for class_obj in classified_objects:
                XA1 = mov_obj.get_bbx()[0].x
                XA2 = mov_obj.get_bbx()[1].x
                YA1 = mov_obj.get_bbx()[0].y
                YA2 = mov_obj.get_bbx()[1].y

                XB1 = class_obj.get_bbx()[0].x
                XB2 = class_obj.get_bbx()[1].x
                YB1 = class_obj.get_bbx()[0].y
                YB2 = class_obj.get_bbx()[1].y

                overlap = max(0, min(XA2, XB2) - max(XA1, XB1)) * max(
                    0, min(YA2, YB2) - max(YA1, YB1)
                )
                A_total_class_obj = (XB2 - XB1) * (YB2 - YB1)
                fraction = overlap / A_total_class_obj

                if fraction > 0.5:
                    self.moving_classified_objects.append(class_obj)
        return self.moving_classified_objects


if __name__ == "__main__":
    m1 = [MovingObject(5, 10, 5, 5, 200, (6, 7))]
    c1 = [ClassifiedObject(8, 13, 4, 4, 20, (4, 3), 0.9, "car")]
    obj_merger = ObjectMerger()
    obj_merger.merge_objects(m1, c1)

