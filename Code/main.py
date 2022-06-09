import pyb, micropython
from pyb import Pin, Timer
from pyb import repl_uart
from ulab import numpy as np
import gc
import pyb
import cotask
import task_share
from stepper import *
from pen import *
import math


class solenoidobj():
    def __init__(self):
        self.drawing = 0

def f(theta):
    return [50*math.cos(theta[0])+50*math.cos(theta[1]) , 50*math.sin(theta[0])+50*math.sin(theta[1])]

def g(x, theta):
    return np.array(x) - np.array(f(theta))

def dg_dtheta(theta):
    return np.array([[50*math.sin(theta[0]), 50*math.sin(theta[1])], [-50*math.cos(theta[0]), -50*math.cos(theta[1])]])

def NewtonRaphson(fcn, jacobian, guess, thresh):
    theta = guess
    while(abs(fcn(theta)[0]) > thresh or abs(fcn(theta)[1]) > thresh):
        theta = theta - np.dot(np.linalg.inv(jacobian(theta)) , fcn(theta))
    return theta

def myraph(dest, guess):
    theta = NewtonRaphson(lambda theta: g(dest,theta), dg_dtheta, guess, 1e-4)
    return theta




def parseHPGL(filename):
    """Takes input hpgl file and outputs double nested list. First list is lines (only 1), second is instructions"""
    im = open(filename, "r")
    lines = im.readline()
    lines = lines.split(";")  #lines[row] becomes another list instead of str
    
    for point in range(len(lines)): #
        lines[point] = lines[point][0:2] + " " + lines[point][2:]
        lines[point] = lines[point].split(',')
        lines[point] = lines[point][0].split(' ') + lines[point][1:]

    return lines

def draw(instr, plotting):
    """Takes instruction in list form ([instruction, points]) from parseHPGL function and fills queue with data """
    interpolated_xy_points = []
    plots = []
    if instr[0] == 'IN':  # IN is ending sequence, first IN must be deleted in HPGL file
        if inshare.get() == 0:
            inshare.put(1)
            xlast.put(0)
            ylast.put(0)
            pass
        else:
            solenoid.put(0)
            X_Vals.put(40)
            Y_Vals.put(0)
            endofinstruction_Vals.put(1)
            endoffile_Vals.put(1)
            colors.put(curcolor.get())
    
    elif instr[0] == 'SP':
        curcolor.put(int(instr[1]))

    elif instr[0] == 'PU':
        plotting.drawing = 0
        interpolated_instr_points = interpolate(instrconv(instr),[xlast.get(), ylast.get()])
        interpolated_xy_points.append(interpolated_instr_points) # converting instruction into points and interpolation of that data
        for i in range(len(interpolated_instr_points)-1):
            solenoid.put(plotting.drawing)
            X_Vals.put(interpolated_instr_points[i][0])
            Y_Vals.put(interpolated_instr_points[i][1])
            colors.put(curcolor.get())
            endofinstruction_Vals.put(0)
            endoffile_Vals.put(0)
        solenoid.put(plotting.drawing)
        X_Vals.put(interpolated_instr_points[-1][0])
        Y_Vals.put(interpolated_instr_points[-1][1])
        colors.put(curcolor.get())
        endofinstruction_Vals.put(1)
        endoffile_Vals.put(0)
        xlast.put(interpolated_instr_points[-1][0])
        ylast.put(interpolated_instr_points[-1][1])

        #x_actuals = [[x[0]/2/math.pi*384,(x[1]+x[0])/2/math.pi*384] for x in interpolated_thetas]

        # funtion to raise solenoid
        # loop to move through target locations

    elif instr[0] == 'PD':
        plotting.drawing = 1
        interpolated_instr_points = interpolate(instrconv(instr),[xlast.get(), ylast.get()])
        interpolated_xy_points.append(interpolated_instr_points) # converting instruction into points and interpolation of that data
        for i in range(len(interpolated_instr_points)-1):
            solenoid.put(plotting.drawing)
            X_Vals.put(interpolated_instr_points[i][0])
            Y_Vals.put(interpolated_instr_points[i][1])
            colors.put(curcolor.get())
            endofinstruction_Vals.put(0)
            endoffile_Vals.put(0)
        solenoid.put(plotting.drawing)
        X_Vals.put(interpolated_instr_points[-1][0])
        Y_Vals.put(interpolated_instr_points[-1][1])
        colors.put(curcolor.get())
        endofinstruction_Vals.put(1)
        endoffile_Vals.put(0)
        xlast.put(interpolated_instr_points[-1][0])
        ylast.put(interpolated_instr_points[-1][1])

        #x_actuals = [[x[0]/2/math.pi*384,(x[1]+x[0])/2/math.pi*384] for x in interpolated_thetas]

        #interpolate()
        # funcion to drop solenoid
        # loop to move through target locations
        
    #return interpolated_xy_points

def instrconv(instr):
    """Takes Output of interpolate function as input and outputs corresponding x,y coord for interpolation func. """
    instr = instr[1:]  # cuts off "PU" & "PD"
    i = 0
    target = [0]*2
    motor_in = []
    if instr[0] == '':
        return [[0,0]]
    while(i < len(instr)):
        target[0] = int(instr[i])
        target[1] = int(instr[i+1])
        motor_in.append([target[0], target[1]])
        i += 2
    return motor_in

def interpolate(targets, curr_location, resolution = 1):  # too many points for memory right now
    """takes a list of targets [[x,y], ...] and current location and returns a new list 
    with as many points to 
    match the desired resolution. Resolution is in dots per inch(dpi)."""
    if len(curr_location) != 2:  # curr_location must be [x,y] 
        print("not a valid current location")
        return None
    interpolated_list = []
    targets.insert(0, [curr_location[0], curr_location[1]])
    for i in range(len(targets)-1):  # want to interpolate between all items in list
        interpolated_list.append(targets[i])  # always add current target
        x_old, y_old = targets[i][0], targets[i][1]
        x_new, y_new = targets[i+1][0], targets[i+1][1]
        distance_x = x_new - x_old
        distance_y = y_new - y_old
        hyp = math.sqrt(distance_x**2 + distance_y**2)
        num_steps = hyp*resolution
        if num_steps == 0:
            curr_location = [x_new, y_new]
            interpolated_list.append([curr_location[0], curr_location[1]])
        else:
            delta_x = distance_x/(num_steps)
            delta_y = distance_y/(num_steps)
            increment = float(1) / resolution  # increment defines how much our motor should move per point after interpolating
            for i in range(int(num_steps-1)):
                    curr_location[0] = curr_location[0] + delta_x
                    curr_location[1] = curr_location[1] + delta_y
                    interpolated_list.append([curr_location[0], curr_location[1]])
            curr_location = [x_new, y_new]
    interpolated_list.append([targets[-1][0],targets[-1][1]])
    return interpolated_list

def pcalc(a_max, ramp_div, pulse_div):  ## is this a motor1.pcalc func now??
    for pmul in range(128,256,1):
        for j in range(14):
            pdiv = 8*(2**j)
            p = a_max/(128*(2**(ramp_div-pulse_div)))
            pd = pmul/pdiv
            q = pd/p
            if(0.95 < q and 1 > q):
                return pmul, j
    return

def TaskFindThetas():
    theta = []
    lastthet1 = math.pi/4
    lastthet2 = math.pi/6
    col = 2
    while True:
        if X_Vals.num_in() > 0:
            curx = X_Vals.get()+60
            cury = Y_Vals.get()
            theta = myraph([curx,cury], [lastthet1, lastthet2])  # converting target(x,y) -> target(theta1, theta2)
            
            #small arm theta calcs
            if theta[0] > 0:
                theta[0] = theta[0] % (math.pi*2)
                if theta[0] > math.pi:
                    theta[0] = theta[0] - (math.pi*2)
            else:
                theta[0] = theta[0] % (math.pi*2)
                if theta[0] > math.pi:
                    theta[0] = theta[0] - (math.pi*2)

            #small arm theta calcs
            if theta[1] > 0:
                theta[1] = theta[1] % (math.pi*2)
                if theta[1] > math.pi:
                    theta[1] = theta[1] - (math.pi*2)
            else:
                theta[1] = theta[1] % (math.pi*2)
                if theta[1] > math.pi:
                    theta[1] = theta[1] - (math.pi*2)

            lastthet1 = theta[0]
            lastthet2 = theta[1]
            solenoid1 = solenoid.get()
            end_of_instr = endofinstruction_Vals.get()
            end_file = endoffile_Vals.get()
            colold = col
            col = colors.get()
            stuff = ("{:},{:},{:},{:},{:},{:}\r\n".format(theta[0], theta[1], solenoid1, end_of_instr, end_file, col))
            uart.write(stuff)
            if col != colold:
                refill(col)
                refillcount.put(0)
            TaskMoveMotors(theta[0], theta[1], solenoid1, col)
        yield (0)

def TaskMoveMotors(theta1, theta2, solenoid, color):
    """if solenoid:
        actuaute_solenoid(soelnoid)"""
    if solenoid == 1:
        refillcount.put(refillcount.get()+1)
    if refillcount.get() >= 100:
        refill(color)
        refillcount.put(0)
    motor2.setloc(theta1)
    motor1.setloc(theta2-theta1)
    pyb.delay(10)
    PB8.value(solenoid)
    print(solenoid)

    
def drawwrapper():
    while True:
        if len(listy)>0:
            instr = listy.pop(0)
            draw(instr, plotting)
        yield

def refill(color):
    PB8.value(0)
    motor2.setloc(0)
    motor1.setloc(0)
    pyb.delay(2000)
    PB8.value(1)
    pyb.delay(500)
    PB8.value(0)
    pyb.delay(500)
    PB8.value(1)
    pyb.delay(500)
    PB8.value(0)
    pyb.delay(500)
    PB8.value(1)
    pyb.delay(500)
    PB8.value(0)
            
            
    if color == 0:
        [theta1, theta2] = myraph([60,60], [-1*math.pi/4, math.pi/6])
    else:
        [theta1, theta2] = myraph([60,-50], [-1*math.pi/4, 0])

    #small arm theta calcs
    if theta1 > 0:
        theta1 = theta1 % (math.pi*2)
        if theta1 > math.pi:
            theta1 = theta1 - (math.pi*2)
    else:
        theta1 = theta1 % (math.pi*2)
        if theta1 > math.pi:
            theta1 = theta1 - (math.pi*2)

    #Big arm theta calcs
    if theta2 > 0:
        theta2 = theta2 % (math.pi*2)
        if theta2 > math.pi:
            theta2 = theta2 - (math.pi*2)
    else:
        theta2 = theta2 % (math.pi*2)
        if theta2 > math.pi:
            theta2 = theta2 - (math.pi*2)
            
    motor2.setloc(theta1)
    motor1.setloc(theta2-theta1)
    pyb.delay(2000)
    PB8.value(1)
    pyb.delay(500)
    PB8.value(0)
    pyb.delay(500)
    PB8.value(1)
    pyb.delay(500)
    PB8.value(0)
    pyb.delay(500)
    PB8.value(1)
    pyb.delay(500)
    PB8.value(0)

if __name__ == "__main__":

    #initialize clk pin    
    PC7 = Pin(Pin.cpu.C7, mode = Pin.OUT_PP,)  # PC7 configured for GPIO output
    tim = Timer(3, period = 3, prescaler = 0) #timer3 @ 80MHz
    tim.channel(2, pin = PC7, mode = Timer.PWM, pulse_width = 2)
    PB8 = Pin(Pin.cpu.B8, mode = Pin.OUT_PP)  # solenoid pin
    # configures PC7 for PWM modulation to act as a clock signal

    #initialize cs and en pins
    PC2 = Pin(Pin.cpu.C2, mode = Pin.OUT_PP, value = 1)  #CS1
    PC3 = Pin(Pin.cpu.C3, mode = Pin.OUT_PP, value = 1)  #CS2
    PC4 = Pin(Pin.cpu.C4, mode = Pin.OUT_PP, value = 1)  #EN1
    PC0 = Pin(Pin.cpu.C0, mode = Pin.OUT_PP, value = 1)  #EN2
    
    motor1 = stepper(PC2, PC4)
    motor2 = stepper(PC3, PC0)

    # Create a share and a queue to test function and diagnostic printouts
    xlast = task_share.Share('f', thread_protect = False, name = "share 0")
    
    ylast = task_share.Share('f', thread_protect = False, name = "share 1")
    
    inshare = task_share.Share('I', thread_protect = False, name = "share 2")
    
    refillcount = task_share.Share('I', thread_protect = False, name = "share 3")
    
    curcolor = task_share.Share('I', thread_protect = False, name = "share 4")
    
    colors = task_share.Queue ('I', 1000, thread_protect = False, overwrite = False,
                           name = "Colors")

    X_Vals = task_share.Queue ('f', 1000, thread_protect = False, overwrite = False,
                           name = "X Values")

    Y_Vals = task_share.Queue ('f', 1000, thread_protect = False, overwrite = False,
                           name = "Y Values")

    solenoid = task_share.Queue ('i', 1000, thread_protect = False, overwrite = False,
                           name = "sol")
    endofinstruction_Vals = task_share.Queue ('i', 1000, thread_protect = False, overwrite = False,
                           name = "EOI")
    endoffile_Vals = task_share.Queue ('i', 1000, thread_protect = False, overwrite = False,
                           name = "EOF")

    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    
    listy = parseHPGL("drawing.hpgl")
    plotting = solenoidobj()
    inshare.put(0)
    
    findthet = cotask.Task (TaskFindThetas, name = 'Task_1', priority = 2, 
                         period = 10, profile = True, trace = False)

    rundraw = cotask.Task (drawwrapper, name = 'Task_2', priority = 2,
                         period = 10, profile = True, trace = False)

    uart = pyb.UART(2, 115200)
    uart.init(115200, bits=8, parity=None, stop = 1)

    listy = parseHPGL("drawing.hpgl")
    plotting = solenoidobj()

    #cotask.task_list.append (taskbut)
    cotask.task_list.append(findthet)
    cotask.task_list.append(rundraw)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect ()

    # Run the scheduler with the chosen scheduling algorithm. Quit if any 
    # character is received through the serial port
    vcp = pyb.USB_VCP ()
    while not vcp.any ():
        cotask.task_list.pri_sched()

    # Empty the comm port buffer of the character(s) just pressed
    vcp.read ()
    
    



    