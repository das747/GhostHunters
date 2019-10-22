from skimage import img_as_ubyte  # convert float to uint8
from skimage.color import rgb2gray
import cv2
import imutils


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


