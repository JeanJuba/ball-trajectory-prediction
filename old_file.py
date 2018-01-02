# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 20:45:47 2017

@author: drakonis
"""
import numpy as np
import cv2
import time


cap = cv2.VideoCapture('green_ball.mp4')# 43 frames
print(cap.isOpened())
if cap.isOpened():
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('total_frames', total_frames)
    selected_frames = []
    ballpos=[]
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', 640,480)

    while cap.isOpened():
        ret, frame = cap.read()

        # Checks the frame integrity
        if ret:
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # define range of blue color in HSV
            lower_green = np.array([29,86,6])
            upper_green = np.array([64,255,255])

            mask = cv2.inRange(hsv, lower_green, upper_green)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #print(ballpos)
            if(center !=None):
                ballpos.append(center)

            for i in range(1, len(ballpos)):
                # if either of the tracked points are None, ignore them
                if ballpos[i - 1] is None or ballpos[i] is None:
                    continue

                # otherwise, compute the thickness of the line and
                # draw the connecting lines
                #thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
                cv2.line(frame, ballpos[i - 1], ballpos[i], (0, 0, 255), 1)
            cv2.imshow('image', frame)
            time.sleep(0.25)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            #print(ballpos)
            break
    print('########################################')
    print('total lenght', len(ballpos))
    cap.release()
    cv2.destroyAllWindows()

    selected_frames = ballpos[2:13]
    print('selected_frames', selected_frames)
    x = []
    y = []
    for i in range(len(selected_frames)):
        x.append(selected_frames[i][0])
        y.append(selected_frames[i][1])
    print('x', x)
    print('y', y)
    print("##########################################")
    #print('interpolação:', np.interp(1017, x, y))
    #cap = cv2.VideoCapture('ball.mp4')
