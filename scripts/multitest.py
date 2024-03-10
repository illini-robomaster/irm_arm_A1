#!/usr/bin/env python3
import time
import keyboard

from ctypes import cdll

import utils
from utils import Types as T

def motor_init(id, mode, trq, W, Pos, K_P, K_W):
    motor = MOTOR_send()
    motor.id = id       # Motor id
    motor.mode = mode   # Mode: 0 is stop, 5 is open-loop slow rotation, 10 is close-loop control
    motor.trq = trq     # Feedforward torque
    motor.W = W         # Angular velocity
    motor.Pos = Pos     # Angle position
    motor.K_P = K_P     # parameter for PID (KP for position mode and zero for velocity mode)
    motor.K_W = K_W     # parameter in PID (KD for position mode and KP for velocity mode)
    return motor

fd = utils.c.open_set(utils.bport)
c = utils.c_init_bare(utils.so)

K_P = 0     # Kp in position mode, set to zero for velocity mode
K_W = 15    # Kd in position mode and Kp in velocity moode

# initilization
motor0_s = motor_init(id=0, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
motor1_s = motor_init(id=1, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
motor2_s = motor_init(id=2, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)

motor0_r = T.MOTOR_recv()
motor1_r = T.MOTOR_recv()
motor2_r = T.MOTOR_recv()

const = 2 * 0.314 * 9.1  # 9.1 is a ratio to consider
MOTOR0_SPEED = const
MOTOR1_SPEED = const
MOTOR2_SPEED = -const  # invert because of the orientation of the arm

print('START')
print('START')
print('r -> Exit')
print('p -> Pause')
print('c -> Continue')
print('w -> Forward')
print('s -> Backward')
try:
    freq = 1 / 100
    paused = False
    while True:
        if keyboard.is_pressed('r'):
            break
        # Pause.
        elif keyboard.is_pressed('p'):
            motor0_s.mode = 0
            motor1_s.mode = 0
            motor2_s.mode = 0
            paused = True
        # Continue.
        elif keyboard.is_pressed('c'):
            motor0_s.mode = 10
            paused = False
        elif paused:
            continue

        # base motor turn left
        if keyboard.is_pressed('k'):
            motor0_s.W = MOTOR0_SPEED
        # base motor turn right
        elif keyboard.is_pressed('l'):
            motor0_s.W = -MOTOR0_SPEED  
        else:
            motor0_s.W = 0.0

        # large arm motor forward
        if keyboard.is_pressed('w'):
            motor1_s.W = MOTOR1_SPEED
        # large arm motor backward
        elif keyboard.is_pressed('s'):
            motor1_s.W = -MOTOR1_SPEED
        else:
            motor1_s.W = 0.0
            motor1_s.K_W = 20

        # small arm motor forward
        if keyboard.is_pressed('q'):
            motor2_s.W = MOTOR2_SPEED
        # small arm motor backward
        elif keyboard.is_pressed('a'):
            motor2_s.W = -MOTOR2_SPEED
        else:
            motor2_s.W = -1.0
            motor2_s.K_W = 20

        if (motor0_s.W, motor1_s.W, motor2_s.W) != (0, 0, 0):
            print('Current position:', motor0_s.Pos)
        # need to modify data before send
        c.modify_data(T.byref(motor0_s))
        c.modify_data(T.byref(motor1_s))
        c.modify_data(T.byref(motor2_s))
        # send out struct command to motors
        c.send_recv(fd, T.byref(motor0_s), T.byref(motor0_r))
        c.send_recv(fd, T.byref(motor1_s), T.byref(motor1_r))
        c.send_recv(fd, T.byref(motor2_s), T.byref(motor2_r))

        time.sleep(freq)
finally:
    motor0_s.mode = 0
    motor1_s.mode = 0
    motor2_s.mode = 0
    c.modify_data(T.byref(motor0_s))
    c.send_recv(fd, T.byref(motor0_s), T.byref(motor0_r))
    c.close_serial(fd)
    print('END')

if __name__ == '__main__':
    main()

