from turtle import color
import serial
import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.animation import FuncAnimation

def main():
    ser = serial.Serial('COM4', 115200)
    ser.flush
    vals = [0,0,0,0,0,0]
    thets = []
    plot = []
    color = []
    i = 0


    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)
    while vals[4] != 1:
        print("Waiting for instruction")
        vals = [0,0,0,0,0,0]
        while vals[3] != 1:
            if ser.in_waiting > 1:
                read = str(ser.readline())[2:-5]
                vals = read.split(',')
                vals = [float(val) for val in vals]
                thets.append([vals[0], vals[1]])
                plot.append(vals[2])
                color.append(vals[5])

                #live animation
                ax.lines.clear()
                theta = thets[i]
                x = [math.cos(theta[0])+ math.cos(theta[1]) for theta in thets]
                y = [math.sin(theta[0])+ math.sin(theta[1]) for theta in thets]
                for j in range(len(thets[:i])-1):
                    if plot[j] == 1 and plot[j+1] == 1 and color[j] == 1:
                        ax.plot([x[j],x[j+1]],[y[j],y[j+1]], color = "blue")
                    elif plot[j] == 1 and plot[j+1] == 1 and color[j] == 0:
                        ax.plot([x[j],x[j+1]],[y[j],y[j+1]], color = "red")
                x1 = [0,math.cos(theta[0])]
                y1 = [0,math.sin(theta[0])]
                x2 = [math.cos(theta[0]), math.cos(theta[0])+ math.cos(theta[1])]
                y2 = [math.sin(theta[0]), math.sin(theta[0])+ math.sin(theta[1])]
                ax.plot(x1,y1,x2,y2, color = "red")
                plt.show(block = False)
                plt.pause(0.00001)
                i += 1
    plt.close()
    fig, ax = plt.subplots()
    print(thets)
    x = [math.cos(theta[0])+ math.cos(theta[1]) for theta in thets]
    y = [math.sin(theta[0])+ math.sin(theta[1]) for theta in thets]

    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-2,2)
    ax.set_ylim(-2,2)

    def animate(i):
        ax.lines.clear()
        theta = thets[i]
        for j in range(len(thets[:i])-1):
            if plot[j] == 1 and plot[j+1] == 1 and color[j] == 1:
                ax.plot([x[j],x[j+1]],[y[j],y[j+1]], color = "blue")
            elif plot[j] == 1 and plot[j+1] == 1 and color[j] == 0:
                ax.plot([x[j],x[j+1]],[y[j],y[j+1]], color = "red")
        x1 = [0,math.cos(theta[0])]
        y1 = [0,math.sin(theta[0])]
        x2 = [math.cos(theta[0]), math.cos(theta[0])+ math.cos(theta[1])]
        y2 = [math.sin(theta[0]), math.sin(theta[0])+ math.sin(theta[1])]
        ax.plot(x1,y1,x2,y2, color = "red")
        return theta

    anim = FuncAnimation(fig,animate,interval = 1, frames = len(thets))
    anim.save("func.gif", fps = 30)
    plt.close()

    plt.figure(1)
    theta_1, = plt.plot(range(len(thets)), [theta[1] for theta in thets])
    theta_0, = plt.plot(range(len(thets)), [theta[0] for theta in thets])
    plt.legend([theta_0, theta_1], ["theta 0", "theta 1"])
    plt.show()

main()