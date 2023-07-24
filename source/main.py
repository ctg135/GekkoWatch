import cv2

cam = cv2.VideoCapture(0)

result, image = cam.read()

if result:
    cv2.imshow('Test', image)
    cv2.waitKey(0)
    cv2.destroyWindow("GeeksForGeeks")
else: print(f'Error of capturing ({result})')

del(cam)