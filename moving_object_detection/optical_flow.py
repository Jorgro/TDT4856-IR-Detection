from typing import Union
import cv2
import numpy as np


class OpticalFlow:
    def __init__(self) -> None:
        self.prev_image = None

    def run(self, new_image: np.array) -> Union[None, np.array]:
        """ Takes in a new image and keeps track of the previously supplied image to calculate the optical flow between them.

        Args:
            new_image (np.array): New image to calculate optical flow between this and the previous image.

        Returns:
            Union[None, np.array]: None if no previous image has been supplied, else
            HSV image of optical flow.
        """
        # Image with same dimension as frame, filled with zeros
        mask = np.zeros_like(new_image)
        if len(new_image.shape) > 1:
            new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

        if self.prev_image is None:
            self.prev_image = new_image
            return

        # Calculate flow
        flow = cv2.calcOpticalFlowFarneback(
            self.prev_image, new_image, None, 0.5, 3, 15, 3, 5, 1.2, 0
        )

        # Magnitude and angle of 2D vectors
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # Sets image saturation to maximum
        mask[..., 1] = 255

        # Sets the image hue accorting to opt. flow direction
        mask[..., 0] = angle * 180 / (np.pi / 2)

        # Sets image value according to opt. flow magnitude
        mask[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)

        return mask


if __name__ == "__main__":
    cap = cv2.VideoCapture("./data/videos/cars.mp4")
    _, first_frame = cap.read()
    _, second_frame = cap.read()

    optflow = OpticalFlow()
    optflow.run(first_frame)
    opt_flow_image = optflow.run(second_frame)
    cv2.imwrite("./data/images/test_optflow_image.png", opt_flow_image)

