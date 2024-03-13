#!/usr/bin/env python3
import time

import util
from util import Motor

def main():
    fd = util.cdll.open_set(util.bport)
    cdll = util.cdll_bare
    try:
        K_P = 0.1   # Kp
        K_W = 5     # Kd
        # Initialize motors
        motors = [Motor(cdll, fd, id_=i,
                        mode=10, T=0.0, W=0.0, Pos=0,
                        K_P=K_P, K_W=K_W)
                  for i in range(3)]

        # Set motors to their starting positions.
        for motor in motors:
            motor.send()
        time.sleep(2)

        print('START')
        # Set motors to a new position
        new_position = {'Pos': 3.14 * 9.1 / 2}
        for motor in motors:
            motor.set_state_send(**new_position)
            motor.send()
        time.sleep(5)

        # End test.
        for motor in motors:
            motor.stop()
    finally:
        c.close_serial(fd)
        print('END')

if __name__ == '__main__':
    main()
