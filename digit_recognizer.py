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


def get_digit(vs, model):
    frame = vs.read()
    frame = imutils.resize(frame, width=600)
    cv2.imwrite("num.jpg", frame)
    im_orig = cv2.imread("num.jpg")
    im_gray = rgb2gray(im_orig)
    img_gray_u8 = img_as_ubyte(im_gray)

    (thresh, im_bw) = cv2.threshold(img_gray_u8, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # resize using opencv
    img_resized = cv2.resize(im_bw, (28, 28))
    ##########################################################
    # invert image
    im_gray_invert = 255 - img_resized
    ####################################
    im_final = im_gray_invert.reshape(1, 28, 28, 1)

    ans = model.predict(im_final)

    ans = ans[0].tolist().index(max(ans[0].tolist()))
    return ans

if __name__ == '__main__':
    model = load_model('mnist_trained_model.h5')  # import CNN model weight

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--picamera", type=int, default=-1,
                    help="whether or not the Raspberry Pi camera should be used")
    ap.add_argument("-a", "--autoscan", type=str, default='no',
                    help='enable auto scanning')
    args = vars(ap.parse_args())

    vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
    time.sleep(1.0)
    while True:
        print('ready')
        if args['autoscan']=='yes' or input():
            print(get_digit(vs, model))
            sleep(1)
    
    
