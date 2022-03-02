from dataclasses import dataclass
from re import X
from typing import Dict, List, Tuple
import cv2
import numpy as np
from moving_object_detection.optical_flow import OpticalFlow
import uuid
from moving_object_detection.utils import threshold_image
from utils import Point


class MovingObject:
    UID = 1

    def __init__(self, x: int, y: int, w: int, h: int, area: float, center: np.array):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area = area
        self.center = center
        self.positions: List[np.array] = [self.center]
        self.updated = True
        self.unique_id = MovingObject.UID
        MovingObject.UID += 1

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
        return f"MovingObject({self.center[0]},{self.center[1]})"


class MovingObjectDetector:
    def __init__(self, area_threshold: int = 3000) -> None:
        self.area_threshold = area_threshold
        self.moving_objects: List[MovingObject] = []
        self.opt_flow = OpticalFlow()
        self.thresholded_image = None

    def run(self, input_image: np.array) -> None:
        self.opt_flow_image = self.opt_flow.run(input_image)
        if self.opt_flow_image is None:
            return
        self.thresholded_image = threshold_image(
            self.opt_flow_image[..., 2]
        )  # The third channel of HSV is Value (intensity) which we will use as a grayscale.
        self.connected_components_labeling()

    def connected_components_labeling(self) -> None:
        connected_components = cv2.connectedComponentsWithStats(
            self.thresholded_image, 4
        )
        (num_labels, labels, stats, centroids) = connected_components

        # To be able to remove them if they aren't updated
        for obj in self.moving_objects:
            obj.updated = False

        # Skipping label 0 as this is always the background
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]

            # Only care about larger objects
            if area > self.area_threshold:
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]
                center = np.array(centroids[i])
                # mask = labels == i
                self.associate_objects(x, y, w, h, area, center)

        # Remove any objects which weren't updated
        for obj in self.moving_objects:
            if not obj.updated:
                self.moving_objects.remove(obj)

    def get_image_with_bounding_boxes(self, image: np.array):
        output = image.copy()
        for i, obj in enumerate(self.moving_objects):
            cv2.rectangle(
                output, (obj.x, obj.y), (obj.x + obj.w, obj.y + obj.h), (0, 255, 0), 3
            )
            cv2.circle(
                output, (int(obj.center[0]), int(obj.center[1])), 4, (0, 0, 255), -1
            )
            cv2.putText(
                output,
                f"Moving Object {obj.unique_id}",
                (obj.x, obj.y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                255,
                4,
            )
        return output

    def associate_objects(self, x, y, w, h, area, center):
        X = np.zeros((len(self.moving_objects), 7))
        for i, obj in enumerate(self.moving_objects):
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
                self.moving_objects[min_index].update(x, y, w, h, area, center)
                return
        self.moving_objects.append(MovingObject(x, y, w, h, area, center))


if __name__ == "__main__":
    cap = cv2.VideoCapture("./data/videos/cars.mp4")
    # print(cap.get(cv2.CAP_PROP_FPS))
    _, first_frame = cap.read()
    _, second_frame = cap.read()
    _, third_frame = cap.read()

    mod = MovingObjectDetector()
    print("Frame 1")
    mod.run(first_frame)
    print("Frame 2")
    mod.run(second_frame)
    print("Frame 3")
    mod.run(third_frame)
    print(mod.moving_objects)
    bb_img = mod.get_image_with_bounding_boxes(third_frame)
    cv2.imwrite("./data/images/bb_image_test.png", bb_img)

    # opt = OpticalFlow()
    # opt.run(first_frame)
    # img = opt.run(second_frame)
    # ret = MovingObjectDetector.threshold_image(img[..., 2])
    # cv2.imwrite("./data/images/test_threshold_otsu.png", ret)

