# Rob Boss - Painting Robot (Disciple of Bob Ross)
#### Contibutors: Vincent Pierce, Conrad Kinsey, Hayden Jeanor

## Overview
Rob Boss (disciple of Bob Ross) is a 2 and a half degree of freedom pen-plotting robot with a twist. This robot is capable of painting whatever digital image(in HPGL format) you give it. The project was created for our ME 405 Mechatronics term project at California Polytechnic State University San Luis Obipso.

With a STM32 Arm Cortex MCU on a Nucleo-64 board as the brains of the robot, we designed a surrounding electro-mechanical system from scratch to bring the software running on the STM32 to life. The [Mechanical Design](https://github.com/VincentPierc/Rob-Boss_Painting-Bot#mechanical-design) section outlines the mechanical design parameters, struggles, and final outcomes for the project. The same for the software architecture can be found in the [Software Design](https://github.com/VincentPierc/Rob-Boss_Painting-Bot#software-design) section.

## Mechanical Design
![Armature View](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/88ab612ea1562960c5a3bc2b429fb5e3f99f7837/IMG_6601%20(1).jpg)

Top down view of robot arm used for drawing. Mechanical design implemented a theta-theta rotation about 2 pivot points, which when combined with a solenoid produced 2 1/2 degreegs of freedom.

###
![Housing View](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/a82402a915220112e0e8c3c14328565b59842928/IMG_6554.jpg)

Side View of robot housing. Housing was designed so that the arm is ~ 5 inches off canvas it will draw on. Additionally, all electronics (solenoid, STM32, Shoe of Brian and breakout board) including their wiring could be placed out of reach from the rotating arm.


## Software Design

### Kinematics
![Animation Drawing](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/135c5ec39ab0f2d908295e72dea60f8ef7972f67/func.gif)

The heart of the Rob's ability to draw lies in our Newton Raphson algorithm which allows us to convert (x, y) coordinates into (theta1,theta2) coordinates. Allowing us to draw images like this flower

![Forward Kinematics](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/dacc0a468a101275a6730d35b857385d50583abe/Capture.PNG)

This conversion or mapping or coordinate systems is considered kinematics and deals with how driving actuators (motors) affects end-effector coordinates (pen-plotter position). Newton Raphson allows us to iteratively solve for motor coordinates which produce x, y coordinates closer and closer to our target position.

![Animated Draw](https://github.com/VincentPierc/Rob-Boss_Painting-Bot/blob/88ee3497bf4c97057412c553574a73d7027e8e55/cross.gif)

Above is the computer animation of Rob drawing a cross, below is a link to a video of Rob actually drawing. The video had to be cut short in order to be uploaded to github.

![Rob Drawing Cross](IMG_6560.MOV)
