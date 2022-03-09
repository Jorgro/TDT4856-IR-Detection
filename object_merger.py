from typing import List
from object_classifier.classified_object import ClassifiedObject
import numpy as np
from object import Object


class ObjectMerger:
    @staticmethod
    def get_overlap(obj1: Object, obj2: Object):
        XA1 = obj1.get_bbx()[0].x
        XA2 = obj1.get_bbx()[1].x
        YA1 = obj1.get_bbx()[0].y
        YA2 = obj1.get_bbx()[1].y

        XB1 = obj2.get_bbx()[0].x
        XB2 = obj2.get_bbx()[1].x
        YB1 = obj2.get_bbx()[0].y
        YB2 = obj2.get_bbx()[1].y

        overlap = max(0, min(XA2, XB2) - max(XA1, XB1)) * max(
            0, min(YA2, YB2) - max(YA1, YB1)
        )
        return overlap

    def merge_objects(
        self, moving_objects: List[Object], classified_objects: List[ClassifiedObject],
    ):
        self.moving_classified_objects: List[Object] = []

        for mov_obj in moving_objects:

            for class_obj in classified_objects:
                overlap = ObjectMerger.get_overlap(mov_obj, class_obj)
                fraction = overlap / class_obj.area

                if fraction > 0.5:
                    self.moving_classified_objects.append(class_obj)

        return self.moving_classified_objects

    def merge_objects_with_threshold(
        self, threshold_img: np.array, classified_objects: List[ClassifiedObject],
    ):
        self.moving_classified_objects: List[ClassifiedObject] = []

        for class_obj in classified_objects:

            X1 = class_obj.get_bbx()[0].x
            X2 = class_obj.get_bbx()[1].x
            Y1 = class_obj.get_bbx()[0].y
            Y2 = class_obj.get_bbx()[1].y

            A_total_class_obj = (X2 - X1) * (Y2 - Y1)

            bbx = threshold_img[Y1:Y2, :]
            bbx = bbx[:, X1:X2]

            non_zero = np.count_nonzero(bbx)

            fraction = non_zero / A_total_class_obj

            if fraction > 0.25:
                self.moving_classified_objects.append(class_obj)
        return self.moving_classified_objects

    def associate_objects(self, x, y, w, h, area, center):
        X = np.zeros((len(self.moving_classified_objects), 7))
        for i, obj in enumerate(self.moving_classified_objects):
            dx = abs(obj.x - x)
            dy = abs(obj.y - y)
            dw = abs(obj.w - w)
            dh = abs(obj.h - h)
            dx_c = abs(obj.center[0] - center[0])
            dy_c = abs(obj.center[1] - center[1])
            da = abs(obj.area - area)
            X[i, :] = np.array([dx, dy, dw, dh, dx_c, dy_c, da])

        if X.size > 0:
            # Normalization
            Z = X / np.array([1920, 1080, 1920, 1080, 1920, 1080, 1920 * 1080])
            # Z = (X - np.min(X, axis=0)) / (np.max(X, axis=0) - np.min(X, axis=0))

            # Sum the normalization
            Z_Sum = np.sum(np.abs(Z), axis=1)

            # Find the closest normalization sum score
            min_index = np.argmin(np.sum(np.abs(Z), axis=1))

            # Should have a normalization sum score of < 0.5 to be associated
            if Z_Sum[min_index] < 0.5:
                self.moving_classified_objects[min_index].update(
                    x, y, w, h, area, center
                )
                return
        self.moving_classified_objects.append(Object(x, y, w, h, area, center))

    def run(
        self, moving_objects: List[Object], classified_objects: List[ClassifiedObject]
    ):
        self.merge_objects(moving_objects, classified_objects)

        for mov in moving_objects:
            any_overlap = False
            for cls in classified_objects:
                if ObjectMerger.get_overlap(mov, cls) > 0:
                    any_overlap = True

            if not any_overlap:
                self.moving_classified_objects.append(mov)


if __name__ == "__main__":
    m1 = [Object(5, 10, 5, 5, 200, (6, 7))]
    c1 = [ClassifiedObject(8, 13, 4, 4, 20, (4, 3), 0.9, "car")]
    obj_merger = ObjectMerger()
    obj_merger.merge_objects(m1, c1)
