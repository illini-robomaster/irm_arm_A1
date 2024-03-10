#!/usr/bin/env python3
import time
import keyboard

import util
from util import Motor

def main():
    fd = util.cdll.open_set(util.bport)
    cdll = util.cdll_bare

    K_P = 0     # Kp in position mode, set to zero for velocity mode
    K_W = 15    # Kd in position mode and Kp in velocity moode

    # initilization
    motor0 = Motor(cdll=cdll, fd=fd, id_=0,
                   mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
    motor1 = Motor(cdll=cdll, fd=fd, id_=1,
                   mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
    motor2 = Motor(cdll=cdll, fd=fd, id_=2,
                   mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)

    motors = [motor0, motor1, motor2]

    const = 2 * 0.314 * 9.1  # 9.1 is a ratio to consider
    MOTOR0_SPEED = const
    MOTOR1_SPEED = const
    MOTOR2_SPEED = -const  # invert because of the orientation of the arm

    print('START')
    print('START')
    print('r -> Exit')
    print('p -> Pause')
    print('c -> Continue')
    print('k -> Base left')
    print('l -> Base right')
    print('w -> Large arm forward')
    print('s -> Large arm backward')
    print('q -> Small arm forward')
    print('a -> Small arm backward')
    try:
        freq = 1 / 100
        paused = False
        while True:
            if keyboard.is_pressed('r'):
                break
            # Pause.
            elif keyboard.is_pressed('p'):
                for motor in motors:
                    motor.set_state_send({'mode': 0})
                paused = True
            # Continue.
            elif keyboard.is_pressed('c'):
                for motor in motors:
                    motor.set_state_send({'mode': 10})
                paused = False
            elif paused:
                continue

            # base motor turn left
            if keyboard.is_pressed('k'):
                motor0.set_state_send({'W': MOTOR0_SPEED})
            # base motor turn right
            elif keyboard.is_pressed('l'):
                motor0.set_state_send({'W': -MOTOR0_SPEED})
            else:
                motor0.set_state_send({'W': 0})

            # large arm motor forward
            if keyboard.is_pressed('w'):
                motor1.set_state_send({'W': MOTOR1_SPEED})
            # large arm motor backward
            elif keyboard.is_pressed('s'):
                motor1.set_state_send({'W': -MOTOR1_SPEED})
            else:
                motor1.set_state_send({'W': 0, 'K_W': 20})

            # small arm motor forward
            if keyboard.is_pressed('q'):
                motor2.set_state_send({'W': MOTOR2_SPEED})
            # small arm motor backward
            elif keyboard.is_pressed('a'):
                motor2.set_state_send({'W': -MOTOR2_SPEED})
            else:
                motor2.set_state_send({'W': 0, 'K_W': 20})

            # No output if all 0s
            if any(motor.get_state_send['W'] for motor in motors):
                for motor in motors:
                    state_send = motor.get_state_send()
                    print('Current position of %s: %s' %
                          (state_send['id'], state_send['Pos']))
            # send out struct command to motors
            for motor in motors:
                motor.send()

            time.sleep(freq)
    finally:
        for motor in motors:
            motor.set_state_send({'mode': 0})
            motor.send()
        cdll.close_serial(fd)
        print('END')

if __name__ == '__main__':
    main()
