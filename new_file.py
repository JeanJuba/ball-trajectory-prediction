import cv2
import time
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt


def interpolation(centers):
    np_array = np.array(centers)
    x = np_array[:,0]
    y = np_array[:,1]
    print('np_array', np_array)
    print('x', x)
    print('y', y)

    plt.gcf().clear()
    plt.gca().invert_yaxis()
    plt.plot(x, y, 'ro', label='original')
    x_new = np.arange(14, 1100, 0.1)
    f = interp1d(x, y, fill_value='extrapolate', kind='cubic')

    y_new = f(x_new)

    plt.plot(x_new, y_new, '--', label='interpolation')
    plt.legend()
    plt.draw()
    #plt.pause(0.2)

    return x_new, y_new


video = cv2.VideoCapture('green_ball.mp4')
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
cv2.resizeWindow('frame', 800, 640)

if video.isOpened():

    center_history = []
    while video.isOpened():
        ret, frame = video.read()
        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            lower_green = np.array([29, 86, 6])
            upper_green = np.array([64, 255, 255])

            mask = cv2.inRange(hsv, lower_green, upper_green)
            contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
            center = None
            if len(contour) > 0:
                c = max(contour, key=cv2.contourArea)
                (x, y), radius = cv2.minEnclosingCircle(c)
                print('radius ', radius)
                print('x', x)
                print('y', y)
                center = int(x), int(y)
                center_history.append(center)
                for i in range(1, len(center_history)):
                    cv2.line(frame, center_history[i - 1], center_history[i], (0, 0, 255), 1)

                if radius > 10:
                    cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)

            print(center_history)
            if len(center_history) > 5:
                x, y = interpolation(center_history)
                points = list(zip(x, y))
                print('points', points)
                cv2.polylines(frame, np.int32([points]), 0,  (0, 255, 255))


            cv2.imshow('frame', frame)
            time.sleep(0.2)



        if cv2.waitKey(1) & 0xFF == ord('q'):
            #print(ballpos)
            break

video.release()
cv2.destroyAllWindows()
