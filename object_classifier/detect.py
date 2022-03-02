from models import *  # set ONNX_EXPORT in models.py
from utils.datasets import *
from utils.utils import *


def detect(image,
           cfg='object_classifier/cfg/yolov3-spp-r.cfg',
           names_data='object_classifier/data/custom.names',
           weights='object_classifier/weights/best.pt',
           img_size=416,
           conf_thres=0.3,
           nms_thres=0.5,
           half=True,
           device=''):
    """
    Does inference on the input image and returns detections in the form of coordinates for BB, 
    confidence and classification
    """

    # Initialize
    device = torch_utils.select_device(device)

    # Initialize model
    model = Darknet(cfg, img_size)

    # Load weights
    attempt_download(weights)
    if weights.endswith('.pt'):  # pytorch format
        model.load_state_dict(
            torch.load(weights, map_location=device)['model'])
    else:  # darknet format
        _ = load_darknet_weights(model, weights)

    # Eval mode
    model.to(device).eval()

    # Half precision
    half = half and device.type != 'cpu'  # half precision only supported on CUDA
    if half:
        model.half()

    # Padded resize
    img = letterbox(image, new_shape=img_size)[0]

    # Normalize RGB
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
    img = np.ascontiguousarray(
        img, dtype=np.float16 if half else np.float32)  # uint8 to fp16/fp32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0

    # Get classes and colors
    classes = load_classes(names_data)

    # Run inference and get detections
    img = torch.from_numpy(img).to(device)
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    pred = model(img)[0]

    if half:
        pred = pred.float()

    # Apply NMS
    pred = non_max_suppression(pred, conf_thres, nms_thres)

    # Process detections
    detections = []
    for _, det in enumerate(pred):  # detections per image

        if det is not None and len(det):
            # Rescale boxes from img_size to image size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4],
                                      image.shape).round()

        for *xyxy, conf, _, cls in det:  # info about detection
            top_left_coor = xyxy[:2]
            bottom_right_coor = xyxy[2:4]
            detections.append(
                (top_left_coor, bottom_right_coor, conf, classes[int(cls)]))

    return image, detections


def run(image):
    """
    Runs detection with only forward-pass
    """
    with torch.no_grad():
        return detect(image)


if __name__ == "__main__":
    img = cv2.imread("object_classifier/data/dashboard_cam.jpeg")
    image, detections = run(img)
    print(image)
    print(detections)