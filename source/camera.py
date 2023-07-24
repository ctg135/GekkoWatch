import cv2
import os

PATH_CAPTURED_FOLDER = os.path.join('..', 'capture')

# CAMERA_FPS = cam.get(cv2.CAP_PROP_FPS)
# CAMERA_HEIGHT = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
# CAMERA_WIDTH = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
CAMERA_FPS = 30
CAMERA_HEIGHT = 640
CAMERA_WIDTH = 480

CAMERA_CAPTURE_SUCCESS = 1
CAMERA_CAPTURE_ERROR = -1
CAMERA_CAPTURE_ERROR_BUSY = -2


def capture_photo(name: str):
    '''
    Захватывает фото с камеры.
    Возвращает результат записи и путь до фото
    '''
    filename = os.path.join(PATH_CAPTURED_FOLDER, name)
    check_folder()
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return CAMERA_CAPTURE_ERROR_BUSY, ''

    result, image = cam.read()
    if result:
        cv2.imwrite(os.path.join(PATH_CAPTURED_FOLDER, name), image)
    else:
        return CAMERA_CAPTURE_ERROR, ''

    del(cam)
    return CAMERA_CAPTURE_SUCCESS, filename


def capture_video(name: str, seconds: int):
    '''
    Захватывает видео с камеры.
    Возвращает результат записи и путь до видео
    '''
    filename = os.path.join(PATH_CAPTURED_FOLDER, name)
    check_folder()
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return CAMERA_CAPTURE_ERROR_BUSY, ''

    out = cv2.VideoWriter(filename, 
                        #   cv2.VideoWriter_fourcc(*"MJPG"), 
                          cv2.VideoWriter_fourcc(*'MP4V'),
                          CAMERA_FPS, 
                          (CAMERA_HEIGHT, CAMERA_WIDTH))

    # Запись видео по кадрам
    total_frames = CAMERA_FPS * seconds
    recored_frames = 0

    while cam.isOpened() and recored_frames <= total_frames:
        ret, frame = cam.read()
        if not ret:
            return CAMERA_CAPTURE_ERROR, ''
        out.write(frame)
        recored_frames += 1
    
    del(cam)
    return CAMERA_CAPTURE_SUCCESS, filename

def remove(file_name: str):
    os.remove(file_name)

def check_folder():
    '''
    Проверка наличия папки для загрузки фото и видео
    '''
    if not os.path.exists(PATH_CAPTURED_FOLDER):
        os.mkdir(PATH_CAPTURED_FOLDER)


if __name__ == '__main__':
    pass