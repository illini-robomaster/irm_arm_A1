#!/usr/bin/env python3
import utils

def motor_init(id_, mode, T, W, Pos, K_P, K_W):
    motor = MOTOR_send()
    motor.id = id_       # Motor id
    motor.mode = mode   # Mode: 0 is stop, 5 is open-loop slow rotation, 10 is close-loop control
    motor.T = T         # Feedforward torque
    motor.W = W         # Angular velocity
    motor.Pos = Pos     # Angle position
    motor.K_P = K_P     # kp parameter in PID
    motor.K_W = K_W     # kd parameter in PID
    return motor

# def movement(id, target_T, target_P, target_w, K_P, K_W, fd):
#     motor_send = motor_init(id, 10, target_T, target_w, target_P, K_P, K_W)
#     motor_receive = MOTOR_recv
#     c.modify_data(byref(motor_send))
#     c.send_recv(fd, byref(motor_send), byref(motor_receive))
#     c.extract_data(byref(motor_receive))
#     return motor_receive

def stop(id_, fd):
    motor_send = motor_init(id_, 0, 0, 0, 0, 0, 0)
    motor_receive = MOTOR_recv
    c.modify_data(byref(motor_send))
    c.send_recv(fd, byref(motor_send), byref(motor_receive))
    c.extract_data(byref(motor_receive))
    return motor_receive

def main():
    try:
        c = utils.c_init_bare(utils.so)
        K_P = 0.1   # Kp
        K_W = 5     # Kd
        print('START')
    finally:
        c.close_serial(fd)
        print('END')

if __name__ == '__main__':
    main()
