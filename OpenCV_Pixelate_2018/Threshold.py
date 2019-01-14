import cv2 as cv
import numpy as np

def nothing(x):pass

cap = cv.VideoCapture(0)
cv.namedWindow('videoUI')
cv.createTrackbar('T','videoUI',0,255,nothing)

while(True):
    ret, frame = cap.read()
    vid_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    thresh = cv.getTrackbarPos('T','videoUI');
    vid_bw = cv.threshold(vid_gray, thresh, 255, cv.THRESH_BINARY)[1]

    cv.imshow('videoUI',cv.flip(vid_bw,1))

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
