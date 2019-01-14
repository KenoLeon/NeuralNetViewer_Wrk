import cv2 as cv
import numpy as np

def nothing(x):pass

cap = cv.VideoCapture(0)

# Get Maximum camera resolution
# https://stackoverflow.com/questions/18458422/query-maximum-webcam-resolution-in-opencv

W = 1000
H = 1000

cap.set(cv.CAP_PROP_FRAME_WIDTH, W)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, H)

fWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
fHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

cv.namedWindow('videoUI', cv.WINDOW_NORMAL)
cv.createTrackbar('T','videoUI',0,255,nothing)
cv.createTrackbar('R','videoUI',0,fHeight,nothing)
cv.setTrackbarPos('R','videoUI',fHeight-1)

while(True):
    ret, frame = cap.read()
    vid_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    HW = cv.getTrackbarPos('R','videoUI')
    thresh = cv.getTrackbarPos('T','videoUI')
    vid_bw = cv.threshold(vid_gray, thresh, 255, cv.THRESH_BINARY)[1]
    flipped = cv.flip(vid_bw,1)
    res = cv.resize(flipped, (HW+1,HW+1))
    cv.imshow('videoUI',res)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
