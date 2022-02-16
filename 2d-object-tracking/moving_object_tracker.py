# https://machinelearningspace.com/2d-object-tracking-using-kalman-filter/

# Need to associate objects from frame to frame.
# Have some distance measurement between the object features.

# Multiple Object Tracking (MOT) evaluation metric:
# 1. Recall: percentage of correctly detected targets, compared to the ground truth
# 2. Precision: percentage of correctly detected targets, compared to all detected objects.
# 3. FAR: number of false alarms per frame, number of false positives divided by total number of frames.
# 4. FP: number of false positives
# 5. IDs: number of ID switches. ID switches happens when a person is detected as different person due to missed
# association or is it was occluded by other object
# 6. FN: number of missed targets
# MOTA: multi-object tracking accuracy in [0,100], MOTA = 1 – error, where error is defined as the total
# number of FN+FP+IDs compared to the total number of ground truth objects.

class MultipleObjectTracker:

    def __init__(self):
        pass
