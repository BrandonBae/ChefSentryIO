# import required libraries
import cv2

# Reading the Image

def detect_humans(image_path: str):
    image = cv2.imread('./resources/images/cooker.jpg')

    # initialize the HOG descriptor
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # detect humans in input image
    (humans, _) = hog.detectMultiScale(image, winStride=(10, 10),
    padding=(32, 32), scale=1.1)

    # getting no. of human detected
    print('Human Detected : ', len(humans))
    for (x, y, w, h) in humans:
        pad_w, pad_h = int(0.15 * w), int(0.01 * h)
        cv2.rectangle(image, (x + pad_w, y + pad_h), (x + w - pad_w, y + h - pad_h), (0, 255, 0), 2)

    # display the output image
    cv2.imshow("Image", image)
    return len(humans)