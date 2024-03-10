#!/usr/bin/env python3
import sys
import time

from ctypes import cdll, byref

from typedef import c, MOTOR_send, MOTOR_recv

def motor_init(id, mode, T, W, Pos, K_P, K_W):
    motor = MOTOR_send()
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
    c = utils.c_init_bare()
    try:
        K_P = 0.1   # Kp
        K_W = 5     # Kd
        motor0_s = motor_init(id=0, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)

        motor0_s1 = motor_init(id=0, mode=10, T=0.0, W=0.0, Pos=3.14 * 9.1 / 2, K_P=K_P, K_W=K_W)
        motor0_stop = motor_init(id=0, mode=0, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
        motor0_r = T.MOTOR_recv()

system = platform.system()
if system == 'Windows':
    fd = c.open_set(b'\\\\.\\COM3')
    libPath = 'lib/libUnitree_motor_SDK_Win64.dll'
elif system == 'Linux':
    SERIAL_PREFIX = "usb-FTDI_USB__-__Serial_Converter_"
    dev_basename = "/dev/serial/by-id"
    try:
        path_list = os.listdir(dev_basename)
    except FileNotFoundError:  # Nothing connected
        path_list = []

    dev_paths = (
        os.path.join(dev_basename, path)
        for path in path_list
        if path.startswith(SERIAL_PREFIX)
    )

    try:
        selected_path = next(dev_paths)
    except StopIteration:
        selected_path = ""

    fd = c.open_set(bytes(selected_path, "utf8"))
    maxbit=sys.maxsize
    if platform.uname()[4] == "x86_64":
        if maxbit > 2**32:
            libPath = "lib/libUnitree_motor_SDK_Linux64.so"
            print("Linux 64 bits")
        else:
            libPath = "lib/libUnitree_motor_SDK_Linux32.so"
            print("Linux 32 bits")
    elif platform.uname()[4] == "aarch64":
        if maxbit > 2**32:
            libPath = "lib/libUnitree_motor_SDK_ARM64.so"
            print("ARM 64 bits")
        else:
            libPath = "lib/libUnitree_motor_SDK_ARM32.so"
            print("ARM 32 bits")

        motor2_s = motor_init(id=2, mode=10, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
        motor2_s1 = motor_init(id=2, mode=10, T=0.0, W=0.0, Pos=3.14 * 9.1 / 2, K_P=K_P, K_W=K_W)
        motor2_stop = motor_init(id=2, mode=0, T=0.0, W=0.0, Pos=0, K_P=K_P, K_W=K_W)
        motor2_r = T.MOTOR_recv()

        c.modify_data(T.byref(motor0_s))
        c.modify_data(T.byref(motor1_s))
        c.modify_data(T.byref(motor2_s))

        c.modify_data(T.byref(motor0_s1))
        c.modify_data(T.byref(motor1_s1))
        c.modify_data(T.byref(motor2_s1))

        c.modify_data(T.byref(motor0_stop))
        c.modify_data(T.byref(motor1_stop))
        c.modify_data(T.byref(motor2_stop))

        c.send_recv(fd, T.byref(motor0_s), T.byref(motor0_r))
        c.send_recv(fd, T.byref(motor0_s), T.byref(motor0_r))
        c.send_recv(fd, T.byref(motor1_s), T.byref(motor1_r))
        c.send_recv(fd, T.byref(motor2_s), T.byref(motor2_r))

        print('START')

        time.sleep(2)

        c.send_recv(fd, T.byref(motor0_s1), T.byref(motor0_r))
        c.send_recv(fd, T.byref(motor1_s1), T.byref(motor1_r))
        c.send_recv(fd, T.byref(motor2_s1), T.byref(motor2_r))

        time.sleep(5)

        c.send_recv(fd, T.byref(motor0_stop), T.byref(motor0_r))
        c.send_recv(fd, T.byref(motor1_stop), T.byref(motor1_r))
        c.send_recv(fd, T.byref(motor2_stop), T.byref(motor2_r))
    finally:
        c.close_serial(fd)
        print('END')

if __name__ == '__main__':
    main()
