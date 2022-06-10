# Rob Boss - Painting Robot (Disciple of Bob Ross)
#### Contibutors: Vincent Pierce, Conrad Kinsey, Hayden Jeanor

## Overview
Rob Boss (disciple of Bob Ross) is a 2 1/2 degree of freedom pen-plotting robot with a twist. This robot is capable of painting whatever HPGL file that is uploaded to its hard-drive. The project was created for our ME 405 Mechatronics term project at California Polytechnic State University San Luis Obipso.

With a STM32 Arm Cortex MCU on a Nucleo-64 board as the brains of the robot, we designed a surrounding electro-mechanical system from scratch to give a 3-dimensional structure to the robot. In combination with the software we designed and uploaded on the STM32, the robot arm can paint any image you can draw on illustrating software. The [Mechanical Design](https://github.com/VincentPierc/Rob-Boss_Painting-Bot#mechanical-design) section outlines the mechanical design parameters, struggles, and final outcomes for the project. The same for the software architecture can be found in the [Software Design](https://github.com/VincentPierc/Rob-Boss_Painting-Bot#software-design) section.



## Mechanical Design

### Design Process

Considering all the group members of the project are electrical engineers, we decided to go with a rather basic mechanical design which ended up being rather complex after muliple iterations. The mechanical design of the robot was largely based upon two parameters:

1. adhere to the [kinematics](https://github.com/VincentPierc/Rob-Boss_Painting-Bot#kinematics) of the program we were implementing
    - this required lighter components to be used towards the end of the arm because of the large amount of leverage being produced by the arm being suspended in air
2. design around the materials we had at our disposal or that we could buy on a college student's budget

#### First Iteration
 Because our design was based off the traditional "arm" configuration with a "shoulder" and "elbow" joint, we would need a stepper motor driving each joint. In the first iteration of the robot, we chose to use one large stepper motor to drive the shoulder joint and one smaller stepper motor to drive the elbow joint. This iteration had the placement of the smaller motor at the location of the elbow joint, so it required the motor to be lighter. This would later present torque problems in the future.

 In order to transfer to the motor torque into arm angle movement, simple elbow pieces were created to directly transfer the movement to the arm. The two armatures, main housing, and the motor elblows were designed in solidworks and 3D printed. The first iteration, shown below, failed because the small motor did not produce enough torque to move the small arm.

![First Iteration](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/main/IMG_4101%5B7925%5D.jpg)

#### Redesign
Upon the realizaion that we could not use the small motor, we redesigned the large arm to use a large motor to drive the small arm mounted above the large motor already driving the large arm. Placing the small arm motor at the shoulder joint reduced the weight towards the end of the arms. However, it required the use of a driving belt and parametric pullies.

![Parametric Pully System](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/main/Parametric%20pullies.jpg)

Through the guidance of our fellow classmates who are majoring in mechanical engineering, we did not have to design my own parametric pullies. Rather, we pulled [customizable parametric pullies](https://www.thingiverse.com/thing:16627) from [Thingiverse](https://www.thingiverse.com/) and edited them on [OpenSCAD](https://openscad.org/) to meet our mechanical design needs. In order to have variable tensioning of the drive belt, the holes that mount the small arm motor are rails. This design idea is based upon the way an alternator fastens in a car can be used to tension that drive belt (with the difference that our drive belt can be hand-tensioned with out the need of a tensioning belt).

### Final Implementation
The images below shows the final form of the robot. Many of the parts of the robot were designed to be fastened together using hardware that was found in lab. Each of the [parts](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/tree/main/Rob_Boss_Mechanical_Design) were 3D printed and assembled using the fasteners. Another standout design aspect is the reduction of weight in the armatures while maintaing rigidity using triangular cutouts.

![Final Mechanical Implementation](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/main/Final%20Mechanical%20Implementation.jpg)

#### Paintbrush Actuation
For the half degree of freedom, we chose a lightweight [solenoid actuator](https://www.amazon.com/dp/B07VC5JKYG?psc=1&ref=ppx_yo2ov_dt_b_product_details). This solenoid provides 5N of push/pull force which is plenty to raise and lower a 50 gram paintbrush. The modified paint brush being actuated was threaded into the end of the solenoid plunger.

#### Matching the 2D Kinematics
![Armature View](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/88ab612ea1562960c5a3bc2b429fb5e3f99f7837/IMG_6601%20(1).jpg)

Top down view of robot arm used for drawing. Mechanical design implemented a theta-theta rotation about 2 pivot points, which when combined with a solenoid produced 2 1/2 degreegs of freedom. To satisfy the calculated kinematics, both arms were desgined so that they would have equivalent lenghts from pivot point to pivot point and from pivot point to the center of the paint brush. These lenghts were chosen to be 5 inches because a 10 inch radius covers the desired painting area.

#### Main Housing
![Housing View](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/main/Electrical%20Wiring.jpg)

Side View of robot main housing. The housing was designed so that the arm is ~ 5 inches off canvas it will draw on. Additionally, all electronics (solenoid relay, STM32, Shoe of Brian and breakout board) including their wiring could be securely placed out of reach from the rotating arm.

### Key Takeaways

#### Gear Reduction
Gear reduction from the motor would increased the resolution. The large arm motor ended up having much worse resolution even with microstepping implemented. In hindsight, having the motor drive the arm using another parametric pully system with gear reduction would have resulted in slower painting speed but much better resolution.

#### Don't Reinvent the Wheel
Starting the project, we originally thought that every aspect of the project had to be orginal and designed ourselves. In reality, trying to design gears in solidworks is unecessary waste of time when some else on the internet has already done so and published their work for free. Rather, our time is more well spend desiging our own innovations.

#### Add a Third Dimension
Orgininally, both arms were going ot be desinged using only one dimension. However, the larger arm ended up getting a top which allowed for more stability in the small arm elbow piece that now had two contact points rather than one with barings. The small arm as well as the large arm motor elbow ended up not being so rigid because of the lack of a "3rd dimmension."

## Electrical Design
The three actuating devices (motors and solenoid) of the robot are controlled via an electrical system comprising of a central microcontroller, motor-interfacing breakout board, and power system. The overall wiring between the devices are shown below.

![Wiring Diagram](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/main/Wiring%20Schematic.png)

### Motor Controlling
The motors are being controlled by the microcontroller sending position signals via SPI over the bus connected between the MCU and the motor-interfacing breakout board. The breakout board houses a [TMC2208](https://www.mouser.com/datasheet/2/256/TMC220x_TMC2224_datasheet_Rev1_09-1879275.pdf) stepper motor driver and [TMC4210](https://www.mouser.com/datasheet/2/256/TMC4210_Datasheet_Rev_1_05-1878621.pdf) microcontroller-motordriver interface for each motor. To simplify the complexity of these chips, they convert motor position to SPI signals readable by the MCU and vice versa to get real time motor position and send target motor position.

### Solenoid Actuating
 In order to provide the power needed for the solenoid to acutate, a [solid state relay](https://www.amazon.com/SSR-100DD-Solid-State-Relay-Module/dp/B07PFDJQLV/ref=asc_df_B07PFDJQLV/?tag=hyprod-20&linkCode=df0&hvadid=344109501737&hvpos=&hvnetw=g&hvrand=4678158795194401447&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9031723&hvtargid=pla-731534345491&psc=1&tag=&ref=&adgrpid=69357499895&hvpone=&hvptwo=&hvadid=344109501737&hvpos=&hvnetw=g&hvrand=4678158795194401447&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9031723&hvtargid=pla-731534345491) was used to convert a 3.3V signal from the microcontroller to 12V, 600mA power supply signal.


## Software Design

### Software Architecture
The overarching software archecture uses a cooperative multi-tasking scheduler. Each of the tasks the robot performs was created with the other tasks in consideration. The robot first parses through the file and creates a list with the first element of which being the instruction name and all subsequent elements being the numbers associated with that instruction. The file then runs throught the two processing tasks to interpret the instructions, move the robot, and send the data to the computer.

#### Draw Wrapper
The main task of the assignment is the Draw Wrapper task. While the function is named Draw Wrapper, This is because it calles the draw function. The actual purpose of the task is to iterate through the instruction list and process a single instruction each time it is called. It does so through popping the first value of the instruction list and then calling the draw function on the popped instruction list. It is inside of the draw function that the instruction is processed. If the instruction is an IN instruction, the function will place the initial point of (0,0) into the X_Vals and Y_Vals queues to set the initial location of the motor when it runs. If an IN instruction is called after this, it will be deemed the end of the list and the motors will reset to their fully extended position. If the instruction is SP, the color selected by the SP instruction will be set as thevalue for the shared variable curcolor. If a PD or PU function is recieved, the function will first set the.

#### Find Thetas
When the task is first initialized it generates a list of size 2 that will be used for temporary theta storage. To be more memory efficient, this could have been a float array of size 2. However, the difference between an array of size 2 and a list of size 2 was deemed negligible in this case since it would be reused. After creating the list, the remaining variables representing the initial guesses for the Newton Raphson function and an initial color value.




### Computer Code
For the "Bells and Whistles" of our assignment, we opted to go with a computer software implementation. The code, running simultaneously to the code on the Nucleo, generates various graphs to visualize what Rob is supposed to be doing.  

![code can be found here](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/main/Code/Computer_Code.py)

#### Live Plotting


#### Gif Generation


#### Theta Timeline


### Kinematics
The requirement of the project is to create a robot that draws with two and a half degrees of freedom not using the tradtional cartesian coordinate system. For this project, we impemented a design that has two finite length armatures with variable angles of direction.

![Forward Kinematics](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/dacc0a468a101275a6730d35b857385d50583abe/Capture.PNG)

#### Newton Raphson
Even though the robot works in terms of two angles, all the data parsed from the input (HPGL) file is in terms of cartesian coordinates. The heart of the Rob's ability to draw lies in the Newton Raphson algorithm which allows us to convert (x, y) coordinates into (theta1, theta2) coordinates. Allowing the robot to draw images like the flower drawn below.

![Animation Drawing](flower.gif)

This conversion, or mapping, of coordinate systems is considered kinematics and deals with how driving actuators (motors) affects end-effector coordinates (pen-plotter position). Newton Raphson allows us to iteratively solve for motor coordinates which produce x, y coordinates closer and closer to our target position.

![Animated Draw](cross.gif)

Above is the computer animation of Rob drawing a cross, below is a link to a video of Rob actually drawing. The video had to be cut short in order to be uploaded to github.

[Rob Drawing Cross](https://www.youtube.com/watch?v=Ki1ZRTqjX58)


