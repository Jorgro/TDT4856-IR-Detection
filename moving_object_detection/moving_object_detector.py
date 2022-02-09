from dataclasses import dataclass
from re import X
from typing import List, Tuple
import cv2
import numpy as np
from optical_flow import OpticalFlow
import uuid


@dataclass
class MovingObject:
    x: int
    y: int
    w: int
    h: int
    center_x: int
    center_y: int
    mask: np.array
    unique_id: uuid.UUID = uuid.uuid4()

    def __hash__(self):
        return str(self.unique_id)

class MovingObjectDetector:
    def __init__(self, area_threshold: int = 3000) -> None:
        self.area_threshold = area_threshold
        self.moving_objects: List[MovingObject] = []
        self.opt_flow = OpticalFlow()
        self.thresholded_image = None

    def run(self, input_image: np.array) -> None:
        opt_flow_image = self.opt_flow.run(input_image)
        if opt_flow_image is None:
            return
        self.thresholded_image = MovingObjectDetector.threshold_image(
            opt_flow_image[..., 2], 10
        )  #
        self.connected_components_labeling()

    def connected_components_labeling(self) -> None:
        connected_components = cv2.connectedComponentsWithStats(
            self.thresholded_image, 4
        )
        (num_labels, labels, stats, centroids) = connected_components

        self.moving_objects = []  # Empty list between runs

        # Skipping label 0 as this is always the background
        for i in range(1, num_labels):
            area = stats[i, cv2.CC_STAT_AREA]

            # Only care about larger objects
            if area > self.area_threshold:
                x = stats[i, cv2.CC_STAT_LEFT]
                y = stats[i, cv2.CC_STAT_TOP]
                w = stats[i, cv2.CC_STAT_WIDTH]
                h = stats[i, cv2.CC_STAT_HEIGHT]
                (cX, cY) = centroids[i]
                mask = labels == i
                self.moving_objects.append(
                    MovingObject(x, y, w, h, int(cX), int(cY), mask)
                )

    @staticmethod
    def threshold_image(image: np.array, threshold: int) -> np.array:
        non_black_pixels = np.where((image[:, :] > threshold))
        img = np.zeros((image.shape[0], image.shape[1])).astype(np.uint8)
        img[non_black_pixels] = 255
        return img

    def get_image_with_bounding_boxes(self, original_image: np.array):
        output = original_image.copy()
        for obj in self.moving_objects:
            cv2.rectangle(
                output, (obj.x, obj.y), (obj.x + obj.w, obj.y + obj.h), (0, 255, 0), 3
            )
            cv2.circle(output, (obj.center_x, obj.center_y), 4, (0, 0, 255), -1)
        return output


if __name__ == "__main__":
    cap = cv2.VideoCapture("./data/videos/cars.mp4")
    _, first_frame = cap.read()
    _, second_frame = cap.read()

    mod = MovingObjectDetector()
    mod.run(first_frame)
    mod.run(second_frame)
    bb_img = mod.get_image_with_bounding_boxes(second_frame)
    cv2.imwrite("./data/images/bb_image_test.png", bb_img)

