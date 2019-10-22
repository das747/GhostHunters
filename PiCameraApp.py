#!/usr/bin/env python


# from skimage.io import imread
# from skimage.transform import resize
import numpy as np
# from skimage import data, io
# from matplotlib import pyplot as plt
from skimage import img_as_ubyte  # convert float to uint8
from skimage.color import rgb2gray
import cv2
import datetime
import argparse
import imutils
import time
from time import sleep
from imutils.video import VideoStream
from keras.models import load_model

model = load_model('mnist_trained_model.h5')  # import CNN model weight

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
                help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(1.0)


def ImagePreProcess(im_orig):
    im_gray = rgb2gray(im_orig)
    # io.imshow(im_gray)
    # plt.show()
    img_gray_u8 = img_as_ubyte(im_gray)
    # cv2.imshow("Window", img_gray_u8)
    # io.imshow(img_gray_u8)
    # plt.show()

    (thresh, im_bw) = cv2.threshold(img_gray_u8, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("Window", im_bw)
    # resize using opencv
    img_resized = cv2.resize(im_bw, (28, 28))
    # cv2.imshow("Window", img_resized)
    ############################################################
    # resize using sciikit
    # im_resize = resize(im,(28,28), mode='constant')
    # io.imshow(im_resize)
    # plt.show()
    # cv2.imshow("Window", im_resize)
    ##########################################################
    # invert image
    im_gray_invert = 255 - img_resized
    # cv2.imshow("Window", im_gray_invert)
    ####################################
    im_final = im_gray_invert.reshape(1, 28, 28, 1)

    ans = model.predict(im_final)
    print(ans)

    ans = ans[0].tolist().index(max(ans[0].tolist()))
    print('DNN predicted digit is: ', ans)


def main():
    while True:
        try:
            frame = vs.read()
            frame = imutils.resize(frame, width=600)

            timestamp = datetime.datetime.now()
            ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
            cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.35, (0, 0, 255), 1)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
                cv2.destroyAllWindows()
                vs.stop()
            elif key == ord("t"):
                cv2.imwrite("num.jpg", frame)
                im_orig = cv2.imread("num.jpg")
                ImagePreProcess(im_orig)
            else:
                pass

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            vs.stop()


if __name__ == "__main__":
    main()
