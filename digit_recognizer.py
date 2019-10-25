from skimage import img_as_ubyte  # convert float to uint8
from skimage.color import rgb2gray
import cv2
import argparse
import imutils
from time import sleep
from imutils.video import VideoStream
from keras.models import load_model


def get_digit(vs, model):
    frame = vs.read()  # считываем кадр
    frame = imutils.resize(frame, width=600)  # меняем размер
    cv2.imwrite("num.jpg", frame)  # сохраняем и открываем как изображение
    im_orig = cv2.imread("num.jpg")
    im_gray = rgb2gray(im_orig)  # преобразуем в градации серого
    img_gray_u8 = img_as_ubyte(im_gray)  # преобразуем в байты

    (thresh, im_bw) = cv2.threshold(img_gray_u8, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # ?
    # resize using opencv
    img_resized = cv2.resize(im_bw, (28, 28))  # меняем размер под размерность модели
    ##########################################################
    # интвертируем изображжение
    im_gray_invert = 255 - img_resized
    ####################################
    # меняем структуру под размерность модели
    im_final = im_gray_invert.reshape(1, 28, 28, 1)

    ans = model.predict(im_final)  # само распознавание

    ans = ans[0].tolist().index(max(ans[0].tolist()))  # получаем найденную цифру из результата
    return ans


# тестовый код, распознавание без вывода видеопотока
if __name__ == '__main__':
    model = load_model('mnist_trained_model.h5')  # import CNN model weight

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--picamera", type=int, default=-1,
                    help="whether or not the Raspberry Pi camera should be used")
    # включение непрерывного распознавания
    ap.add_argument("-a", "--autoscan", type=str, default='no',
                    help='enable auto scanning')
    args = vars(ap.parse_args())

    vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
    sleep(1.0)
    while True:
        print('ready')
        # если непрерывное распознавание отключено, распознаём по нажатию enter
        if args['autoscan'] == 'yes' or input():
            print(get_digit(vs, model))
            sleep(1)
