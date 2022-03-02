from object_classifier.detect import ObjectClassifier
import cv2
from moving_object_detection.moving_object_detector import MovingObjectDetector
from object_merger import ObjectMerger

cap = cv2.VideoCapture("./data/videos/cars.mp4")

# print(cap.get(cv2.CAP_PROP_FPS))
_, first_frame = cap.read()
_, second_frame = cap.read()
_, third_frame = cap.read()

mod = MovingObjectDetector()
obc = ObjectClassifier()

mod.run(first_frame)
mod.run(second_frame)
mod_obj = mod.area_threshold
mod_image = mod.get_image_with_bounding_boxes()

img, det = obc.run(second_frame)
merger = ObjectMerger()
merger.merge_objects(mod.moving_objects, det)
new_img =
