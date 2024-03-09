#!/usr/bin/env python3
import os 
import sys
import time
import platform

from ctypes import cdll

from typedef import c

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

system = platform.system()
if system == 'Windows':
    fd = c.open_set(b'\\\\.\\COM3')
    libPath = 'lib/libUnitree_motor_SDK_Win64.dll'
elif system == 'Linux':
    SERIAL_PREFIX = 'usb-FTDI_USB__-__Serial_Converter_'
    dev_basename = '/dev/serial/by-id'
    try:
        path_list = os.listdir(dev_basename)
    except FileNotFoundError:  # Nothing connected
        path_list = []

    dev_paths = (os.path.join(dev_basename, path)
             for path in path_list
             if path.startswith(SERIAL_PREFIX))

    try:
        selected_path = next(dev_paths)
    except StopIteration:
        selected_path = ''

    fd = c.open_set(bytes(selected_path, 'utf8'))
    maxbit=sys.maxsize
    if platform.uname()[4] == "x86_64":
        if maxbit > 2**32:
            libPath = ('lib/libUnitree_motor_SDK_Linux64.so')
            print("Linux 64 bits")
        else:
            libPath = (
                'lib/libUnitree_motor_SDK_Linux32.so'
            )
            print("Linux 32 bits")
    elif platform.uname()[4] == "aarch64":
        if maxbit > 2**32:
            libPath = (
               "lib/libUnitree_motor_SDK_ARM64.so"
            )
            print("ARM 64 bits")
        else:
            libPath = (
               "lib/libUnitree_motor_SDK_ARM32.so"
            )
            print("ARM 32 bits")

c = cdll.LoadLibrary(libPath)
K_P = 0.1   # Kp
K_W = 5     # Kd
print('START')

print('END')

c.close_serial(fd)
