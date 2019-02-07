import cv2
import time
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfile
import os
import ctypes


def get_screen_resolution():
    # OS is Windows
    if os.name is 'nt':
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    else:
        # Other OS
        return 1900, 900


def get_video_file():
    file = askopenfile(initialdir='./')
    if file:
        print(file.name)
        # video_name_field.configure(text=file.name)
        video_name_field.delete(0, END)
        video_name_field.insert(0, file.name)


def interpolation(centers):
    np_array = np.array(centers)
    x = np_array[:, 0]
    y = np_array[:, 1]
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
    # plt.pause(0.2)

    return x_new, y_new


def start_command(v_name='', hsv_lower_lim='', hsv_higher_lim=''):
    # If nothing is passed then the standard are the limits for the green color in hsv
    print(v_name)

    if not hsv_lower_lim.isdigit():
        hsv_lower_lim = 29

    if not hsv_higher_lim.isdigit():
        hsv_higher_lim = 64

    print('hsv lower: %d \nhsv higher: %d' % (int(hsv_lower_lim), int(hsv_higher_lim)))
    if v_name.endswith('.mp4'):
        init(v_name, int(hsv_lower_lim), int(hsv_higher_lim))

    else:
        print('Invalid Format!!!')


def init(video_name, hsv_lower_lim, hsv_higher_lim):
    frame_width = 700
    frame_height = 600

    video = cv2.VideoCapture(video_name)

    lower_lim = [hsv_lower_lim, 50, 50]
    higher_lim = [hsv_higher_lim, 255, 255]

    if video.isOpened():

        center_history = []
        while video.isOpened():
            ret, frame = video.read()
            if ret:
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                frame = cv2.resize(frame, (frame_width, frame_height))

                lower_color = np.array(lower_lim)
                upper_color = np.array(higher_lim)

                resized_mask = cv2.inRange(hsv, lower_color, upper_color)
                mask = cv2.resize(resized_mask, (frame_width, frame_height))

                cv2.namedWindow('HSV Mask')
                cv2.imshow('HSV Mask', mask)
                cv2.moveWindow('HSV Mask', int(get_screen_resolution()[0]/2),
                               int(get_screen_resolution()[1]/2) - int(frame_height/2))
                cv2.resizeWindow('HSV Mask', frame_width, frame_height)

                contour = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
                # center = None
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

                cv2.namedWindow('Identified Object')
                cv2.imshow('Identified Object', frame)
                cv2.moveWindow('Identified Object', int(get_screen_resolution()[0]/2) - frame_width - 30,
                               int(get_screen_resolution()[1]/2) - int(frame_height/2))
                cv2.resizeWindow('Identified Object', frame_width, frame_height)
                time.sleep(0.2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit()

    video.release()
    cv2.destroyAllWindows()


tk = Tk()
tk.title('Ball Trajectory Prediction')

top = Frame(tk)
top.pack(side='top', fill='both', expand='false')

bottom = Frame(tk)
bottom.pack(side='bottom', fill='x', expand='true')

video_name_label = Label(top, text='Video Path: ', width=15, anchor=W)
video_name_label.pack(side='left')

video_name_field = Entry(top, width=60)
video_name_field.pack(side='left', fill='both', expand='true')

button_file = Button(top, text='Find File:', command=get_video_file, width=10)
button_file.pack(side='right')

lower_color_label = Label(bottom, text='Lower HSV Limit: ',  width=15, anchor=W)
lower_color_label.pack(side='left')

lower_color_field = Entry(bottom,  width=10)
lower_color_field.pack(side='left')

higher_color_label = Label(bottom, text='Higher HSV Limit: ', width=15, anchor=W)
higher_color_label.pack(side='left')

higher_color_field = Entry(bottom, width=10)
higher_color_field.pack(side='left')

button_start = Button(bottom, text='Start',  command=lambda: start_command(video_name_field.get(),
                                                                           lower_color_field.get(),
                                                                           higher_color_field.get()), width=10)
button_start.pack(side='right')

width = 720
height = 50

frame_x = (tk.winfo_screenwidth())/2 - width/2
frame_y = (tk.winfo_screenheight())/2 - height/2

tk.geometry('%dx%d+%d+%d' % (width, height, frame_x, frame_y))
tk.mainloop()




