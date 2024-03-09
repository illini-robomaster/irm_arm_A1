#!/usr/bin/env python3
import os 
import sys
from typedef import *
from ctypes import *
import time

def motor_init(id, mode, T, W, Pos, K_P, K_W):
    motor = MOTOR_send()
    motor.id = id       # Motor id
    motor.mode = mode   # Mode: 0 is stop, 5 is open-loop slow rotation, 10 is close-loop control
    motor.T = T         # Feedforward torque
    motor.W = W         # Angular velocity
    motor.Pos = Pos     # Angle position
    motor.K_P = K_P     # kp parameter in PID
    motor.K_W = K_W     # kd parameter in PID
    return motor

def motor_send(fd, send, receive):
    c.send_recv(fd, byref(send), byref(receive))

def read_receive_pos(receive):
    c.extract_data(byref(receive))
    return receive.Pos

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
K_P = 0.1   # Kp
K_W = 5     # Kd
motor0_s = motor_init(id=0, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)

motor0_s1 = motor_init(id=0, mode=10, T=0.0, W=0.0, Pos=3.14 * 9.1 / 2, K_P=K_P, K_W=K_W)
motor0_stop = motor_init(id=0, mode=0, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
motor0_r = MOTOR_recv()

motor1_s = motor_init(id=1, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
motor1_s1 = motor_init(id=1, mode=10, T=0.0, W=0.0, Pos=3.14 * 9.1 / 2, K_P=K_P, K_W=K_W)
motor1_stop = motor_init(id=1, mode=0, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
motor1_r = MOTOR_recv()

motor2_s = motor_init(id=2, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
motor2_s1 = motor_init(id=2, mode=10, T=0.0, W=0.0, Pos=3.14 * 9.1 / 2, K_P=K_P, K_W=K_W)
motor2_stop = motor_init(id=2, mode=0, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
motor2_r = MOTOR_recv()

c.modify_data(byref(motor0_s))
c.modify_data(byref(motor1_s))
c.modify_data(byref(motor2_s))

c.modify_data(byref(motor0_s1))
c.modify_data(byref(motor1_s1))
c.modify_data(byref(motor2_s1))

c.modify_data(byref(motor0_stop))
c.modify_data(byref(motor1_stop))
c.modify_data(byref(motor2_stop))

c.send_recv(fd, byref(motor0_s), byref(motor0_r))
c.send_recv(fd, byref(motor0_s), byref(motor0_r))
c.send_recv(fd, byref(motor1_s), byref(motor1_r))
c.send_recv(fd, byref(motor2_s), byref(motor2_r))

print('START')

time.sleep(2)

c.send_recv(fd, byref(motor0_s1), byref(motor0_r))
c.send_recv(fd, byref(motor1_s1), byref(motor1_r))
c.send_recv(fd, byref(motor2_s1), byref(motor2_r))

time.sleep(5)

c.send_recv(fd, byref(motor0_stop), byref(motor0_r))
c.send_recv(fd, byref(motor1_stop), byref(motor1_r))
c.send_recv(fd, byref(motor2_stop), byref(motor2_r))

print('END')

c.close_serial(fd)