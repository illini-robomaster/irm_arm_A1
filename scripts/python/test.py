#!/usr/bin/env python3
import time
import keyboard

import util
from util import Motor
from util import Types as T

def main():
    fd = util.cdll.open_set(util.bport)
    cdll = util.cdll_bare

    # initilization
    motor = Motor(cdll=cdll, fd=fd, id_=0,
                  mode=10, T=0.0, W=0.0, Pos=0, K_P=0, K_W=2)

    const = 2 * 0.314 * 9.1  # 9.1 is a ratio to consider
    MOTOR0_SPEED = const

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
                motor.set_state_send(mode=0)
                paused = True
            # Continue.
            elif keyboard.is_pressed('c'):
                motor.set_state_send(mode=10)
                paused = False
            elif paused:
                continue
            # large arm motor forward
            if keyboard.is_pressed('w'):
                motor.set_state_send(W=MOTOR0_SPEED)
            # large arm motor backward
            elif keyboard.is_pressed('s'):
                motor.set_state_send(W=-MOTOR0_SPEED)
            else:
                motor.set_state_send(W=0, K_W=20)

            if motor.motor_send.W != 0:
                print('Current position:', motor.get_state_send('Pos'))
            # send out struct command to motor
            motor.send()

            time.sleep(freq)
    finally:
        motor.set_state_send(mode=0)
        motor.send()
        cdll.close_serial(fd)
        print('END')

if __name__ == '__main__':
    main()
