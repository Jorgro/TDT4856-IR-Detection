import numpy as np
import cv2

image = cv2.imread("optflow_images/optflow0.png")
# img = cv2.imread("grayscale.png", cv2.IMREAD_GRAYSCALE)
# thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# cv2.imwrite("threshold.png", thresh)


def threshold_img(img):
    non_black_pixels = np.where(
        (img[:, :, 0] > 10) | (img[:, :, 1] > 10) | (img[:, :, 2] > 10)
    )
    img = np.zeros((1080, 1920, 3))
    img[non_black_pixels] = (255, 255, 255)
    return img


rt = threshold_img(image)
cv2.imwrite("grayscale.png", rt)

thresh = cv2.imread("grayscale.png", cv2.IMREAD_GRAYSCALE)

## CCL:

output = cv2.connectedComponentsWithStats(thresh, 4)
(numLabels, labels, stats, centroids) = output
# loop over the number of unique connected component labels
for i in range(0, numLabels):
    # if this is the first component then we examine the
    # *background* (typically we would just ignore this
    # component in our loop)
    if i == 0:
        text = "examining component {}/{} (background)".format(i + 1, numLabels)
    # otherwise, we are examining an actual connected component
    else:
        text = "examining component {}/{}".format(i + 1, numLabels)
    # print a status message update for the current connected
    # component
    print("[INFO] {}".format(text))
    # extract the connected component statistics and centroid for
    # the current label
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    area = stats[i, cv2.CC_STAT_AREA]
    (cX, cY) = centroids[i]
    print("Area: ", area)

    if area > 3000:

        # clone our original image (so we can draw on it) and then draw
        # a bounding box surrounding the connected component along with
        # a circle corresponding to the centroid
        output = image.copy()
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)
        # construct a mask for the current connected component by
        # finding a pixels in the labels array that have the current
        # connected component ID
        componentMask = (labels == i).astype("uint8") * 255
        # show our output image and connected component mask
        cv2.imshow("Output", output)
        cv2.imwrite("output.png", componentMask)
        cv2.imshow("Connected Component", componentMask)
        cv2.waitKey(0)
