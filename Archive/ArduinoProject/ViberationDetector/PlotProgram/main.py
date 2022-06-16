import serial
import numpy as np
import matplotlib.pyplot as plt

COMPORT = 'COM4'
plt.ion()

ser = serial.Serial(COMPORT, baudrate=115200)

figure, ax = plt.subplots(figsize=(8, 6))

if __name__ == '__main__':
    # create lists to store the data
    data_x = []
    data_y = []
    is_collect = False
    is_finished = False
    is_first_plot = True
    line1 = ''
    while True:
        data = ser.readline().decode()[: -2]

        # judge the data-head
        if data == "BOF":
            is_collect = True
            data = ser.readline().decode()[: -2]
        elif data == "EOF":
            is_collect = False
            is_finished = True

        if is_collect:
            split_data = data.split(",")
            data_x.append(float(split_data[0]))
            data_y.append(float(split_data[1]))

        if is_finished:
            xpoints = np.array(data_x[10:300])
            ypoints = np.array(data_y[10:300])
            print(xpoints)
            print(ypoints)
            if is_first_plot:
                line1, = ax.plot(xpoints, ypoints)
                is_first_plot = False
            else:
                line1.set_xdata(xpoints)
                line1.set_ydata(ypoints)
                figure.canvas.draw()
                figure.canvas.flush_events()

            is_finished = False
            is_collect = False
            data_x = []
            data_y = []







