import cv2
import camera, os

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Cannot open camera")

'''
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*"MJPG"), 30, (640, 480))

len = 0
while cam.isOpened() and len <= 150:
    ret, frame = cam.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # write the flipped frame
    out.write(frame)
    len = len + 1
'''
result, image = cam.read()

if result:
    cv2.imwrite(os.path.join( camera.PATH_CAPTURED_FOLDER, 'kek.png'), image)
else: print(f'Error of capturing ({result})')

del(cam)


