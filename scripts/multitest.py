#!/usr/bin/env python3
import os 
import sys
import time
import keyboard
import platform

from ctypes import cdll

from typedef import c

def motor_init(id, mode, T, W, Pos, K_P, K_W):
    motor = MOTOR_send()
    motor.id = id       # Motor id
    motor.mode = mode   # Mode: 0 is stop, 5 is open-loop slow rotation, 10 is close-loop control
    motor.T = T         # Feedforward torque
    motor.W = W         # Angular velocity
    motor.Pos = Pos     # Angle position
    motor.K_P = K_P     # parameter for PID (KP for position mode and zero for velocity mode)
    motor.K_W = K_W     # parameter in PID (KD for position mode and KP for velocity mode)
    return motor

system=platform.system()
if system == 'Windows':
    fd = c.open_set(b'\\\\.\\COM3')
    libPath = os.path.dirname(os.getcwd()) + '/lib/libUnitree_motor_SDK_Win64.dll'
elif system == 'Linux':
    fd = c.open_set(b'/dev/ttyUSB0')
    maxbit=sys.maxsize
    if maxbit>2**32:
        libPath = os.path.dirname(os.getcwd()) + '/lib/libUnitree_motor_SDK_Linux64.so'
        print('Linux 64 bits')
    else:
        libPath = os.path.dirname(os.getcwd()) + '/lib/libUnitree_motor_SDK_Linux32.so'
        print('Linux 32 bits')

c = cdll.LoadLibrary(libPath)

K_P = 0     # Kp in position mode, set to zero for velocity mode
K_W = 15    # Kd in position mode and Kp in velocity moode

# initilization
motor0_s = motor_init(id=0, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
motor1_s = motor_init(id=1, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
motor2_s = motor_init(id=2, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)

motor0_r = MOTOR_recv()
motor1_r = MOTOR_recv()
motor2_r = MOTOR_recv()

MOTOR0_SPEED = 2 * 0.314*9.1    # 9.1 is a ratio to consider
MOTOR1_SPEED = 2 * 0.314*9.1   # invert because of the orientation of the arm
MOTOR2_SPEED = -2 * 0.314*9.1   # invert because of the orientation of the arm

print('START')

stop = False    # flag for stop
while(True):
    # send
    if (keyboard.is_pressed('p') or stop == True):
        motor0_s.mode = 0
        motor1_s.mode = 0
        motor2_s.mode = 0
        stop = True     # stop motors
        if (keyboard.is_pressed('c')):
            motor0_s.mode = 10
            motor1_s.mode = 10
            motor2_s.mode = 10
            stop = False    # continue
    else:
        if (keyboard.is_pressed("k")):
            motor0_s.W = MOTOR0_SPEED   # base motor turn left
        elif(keyboard.is_pressed("l")):
            motor0_s.W = -MOTOR0_SPEED  # base motor turn right
        else:
            motor0_s.W = 0.0

        if (keyboard.is_pressed("w")):
            motor1_s.W = MOTOR1_SPEED   # large arm motor forward
        elif(keyboard.is_pressed("s")):
            motor1_s.W = -MOTOR1_SPEED  # large arm motor backward
        else:
            motor1_s.W = 0.0
            motor1_s.K_W = 20

        if (keyboard.is_pressed("q")):
            motor2_s.W = MOTOR2_SPEED   # small arm motor forward
        elif(keyboard.is_pressed("a")):
            motor2_s.W = -MOTOR2_SPEED  # small arm motor backward
        else:
            motor2_s.W = -1.0
            motor2_s.K_W = 20
        
    c.modify_data(byref(motor0_s))  # need to modify data before send
    c.modify_data(byref(motor1_s))
    c.modify_data(byref(motor2_s))

    c.send_recv(fd, byref(motor0_s), byref(motor0_r))   # send out struct command to motors
    c.send_recv(fd, byref(motor1_s), byref(motor1_r))
    c.send_recv(fd, byref(motor2_s), byref(motor2_r))

    time.sleep(0.01)
