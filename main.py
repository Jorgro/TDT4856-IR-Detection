from object_classifier.detect import ObjectClassifier
import cv2
from moving_object_detection.moving_object_detector import MovingObjectDetector
from object_merger import ObjectMerger
from object_classifier.classified_object import get_image_with_bbx
from GUI.image_viewer import ImageViewer

cap = cv2.VideoCapture("./data/videos/cars.mp4")

# print(cap.get(cv2.CAP_PROP_FPS))

mod = MovingObjectDetector()
obc = ObjectClassifier()
obj_merger = ObjectMerger()


ret, frame = cap.read()

mod.run(frame)
obc.run(frame)

i = 0
while i < 30:
    ret, frame = cap.read()
    mov_objs = mod.run(frame)
    class_objs = obc.run(frame)
    mov_class_objs = obj_merger.merge_objects(mov_objs, class_objs)

    # Plot bounding boxes of objects in original image

    mov_objs_img = mod.get_image_with_bounding_boxes(frame)
    class_objs_img = get_image_with_bbx(class_objs, frame)
    mov_class_objs_img = get_image_with_bbx(mov_class_objs, frame)
    thresholded_img = mod.thresholded_image.copy()

    main_dir = "./data/GUI_images"
    print("Writing images")
    cv2.imwrite(f"{main_dir}/input/image{i}.png", frame)
    cv2.imwrite(f"{main_dir}/moving_bbxs/image{i}.png", mov_objs_img)
    cv2.imwrite(f"{main_dir}/classified_bbxs/image{i}.png", class_objs_img)
    cv2.imwrite(f"{main_dir}/thresholded/image{i}.png", thresholded_img)
    cv2.imwrite(f"{main_dir}/object_merger/image{i}.png", mov_class_objs_img)

    i += 1


# img = ImageViewer()

