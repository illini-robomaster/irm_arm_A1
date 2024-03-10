#!/usr/bin/env python3
import time
import keyboard

from ctypes import cdll

import utils
from utils import Types as T

def motor_init(id, mode, trq, W, Pos, K_P, K_W):
    motor = T.MOTOR_send()
    motor.id = id       # Motor id
    motor.mode = mode   # Mode: 0 is stop, 5 is open-loop slow rotation, 10 is close-loop control
    motor.trq = trq     # Feedforward torque
    motor.W = W         # Angular velocity
    motor.Pos = Pos     # Angle position
    motor.K_P = K_P     # kp parameter in PID
    motor.K_W = K_W     # kd parameter in PID
    return motor

def main():
    fd = utils.c.open_set(utils.bport)
    c = utils.c_init_bare(utils.so)

    motor0_s = motor_init(id=0, mode=10, trq=0.0, W=0.0, Pos=0, K_P=0, K_W=2)
    motor0_r = T.MOTOR_recv()

    const = 2 * 0.314 * 9.1
    print('START')
    print('r -> Exit')
    print('p -> Pause')
    print('c -> Continue')
    print('w -> Forward')
    print('s -> Backward')
    try:
        freq = 1 / 200
        paused = False
        while True:
            if keyboard.is_pressed('r'):
                break
            # Pause.
            elif keyboard.is_pressed('p'):
                motor0_s.mode = 0
                paused = True
            # Continue.
            elif keyboard.is_pressed('c'):
                motor0_s.mode = 10
                paused = False
            if paused:
                continue

            if keyboard.is_pressed('w'):
                # position = motor0_s.Pos + Delta_position
                # motor0_s.Pos = position
                motor0_s.W = const
            elif(keyboard.is_pressed('s')):
                motor0_s.W = -const
            else:
                motor0_s.W = 0.0

            if motor0_s.W != 0:
                print('Current position:', motor0_s.Pos)
            c.modify_data(T.byref(motor0_s))
            c.send_recv(fd, T.byref(motor0_s), T.byref(motor0_r))
            # receieve
            c.extract_data(T.byref(motor0_r))

            time.sleep(freq)
    finally:
        motor0_s.mode = 0
        c.modify_data(T.byref(motor0_s))
        c.send_recv(fd, T.byref(motor0_s), T.byref(motor0_r))
        c.close_serial(fd)
        print('END')

if __name__ == '__main__':
    main()
