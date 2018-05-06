from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np

from tkinter import *
''''
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [2, 3, 4, 7, 4, 5, 6, 5, 4, 3]

plt.plot(x, y, 'ro', label='original')
x_new = np.arange(1, 15, 0.1)
f = interp1d(x, y, fill_value='extrapolate', kind='cubic')

y_new = f(x_new)

plt.plot(x_new, y_new, '--', label='interpolation')
plt.legend()
plt.show()'''
''''
tk = Tk()
tk.title('Menu')

top = Frame(tk)
top.pack(side='top', fill='both', expand='false')

bottom = Frame(tk)
bottom.pack(side='bottom', fill='x', expand='true')


video_name_field = Label(top, text='Video Path: ', width=15, anchor=W)
video_name_field.pack(side='left')

video_name_field = Entry(top, width=60)
video_name_field.pack(side='left', fill='both')

button_file = Button(top, text='Find File:', width=10)
button_file.pack(side='left')

lower_color_label = Label(bottom, text='Lower HSV Limit: ',  width=15, anchor=W)
lower_color_label.pack(side='left')

lower_color_field = Entry(bottom,  width=10)
lower_color_field.pack(side='left')

higher_color_label = Label(bottom, text='Higher HSV Limit: ', width=15, anchor=W)
higher_color_label.pack(side='left')

higher_color_field = Entry(bottom, width=10)
higher_color_field.pack(side='left')

button_start = Button(bottom, text='Start', width=10)
button_start.pack(side='right')


width = 555
height = 50

frame_x = (tk.winfo_screenwidth())/2 - width/2
frame_y = (tk.winfo_screenheight())/2 - height/2

tk.geometry('%dx%d+%d+%d' % (width, height, frame_x, frame_y))

tk.mainloop()'''

import ctypes
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)