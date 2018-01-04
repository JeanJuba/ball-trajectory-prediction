import cv2
import time
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfile
import os


def get_video_file():
    home = os.path.expanduser('~')
    file = askopenfile(initialdir=home)
    if file:
        print(file.name)
        #video_name_field.configure(text=file.name)
        video_name_field.delete(0, END)
        video_name_field.insert(0, file.name)


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


def start_command(v_name=''):
    print(v_name)
    if v_name.endswith('.mp4'):
        init(v_name)
    else:
        print('Formato inválido!!!')


def init(video_name):
    video = cv2.VideoCapture(video_name)
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
                break

    video.release()
    cv2.destroyAllWindows()


tk = Tk()
tk.title('Ball Trajectory Detection')
video_name_field = Entry(tk, width=50)
video_name_field.grid(row=0, column=0)

button = Button(tk, text='Find File', command=get_video_file, width=8)
button.grid(row=0, column=1)

button_start = Button(tk, text='Start', command=lambda: start_command(video_name_field.get()), width=8)
button_start.grid(row=1, column=1)

width = 366
height = 50

frame_x = (tk.winfo_screenwidth())/2 - width/2
frame_y = (tk.winfo_screenheight())/2 - height/2

tk.geometry('%dx%d+%d+%d' % (width, height, frame_x, frame_y))

print(frame_x, frame_y)

tk.mainloop()


