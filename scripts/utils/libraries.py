import platform

from ctypes import cdll

from .typedef import Types as T

def get_so():
    uname = platform.uname()
    system = uname.system
    machine = uname.machine
    # SOs are named according to (system, bits) tuple.
    if system == 'Windows':
        tup = ('Win', '64')
    elif system == 'Linux':
        # x86_64
        if machine == 'x86_64':
            tup = ('Linux', '64')
        # i?86
        elif machine.endswith('86'):
            tup = ('Linux', '32')
        # aarch32/64
        elif uname.machine.startswith('aarch'):
            tup = ('ARM', machine[:-2])
        # Likely unsupported
        else:
            raise RuntimeError(f'{machine} not supported.')
    else:
        raise RuntimeError(f'{system} not supported.')

    fst, snd = tup
    return f'lib/libUnitree_motor_SDK_{fst}{snd}.so'

def c_init_bare(so):
    return cdll.LoadLibrary(so)

def c_init(so):
    c = c_init_bare(so)

    # motor_ctrl.h
    c.getSystemTime.restype = T.c_longlong

    c.modify_data.restype = T.c_int32
    c.modify_data.argtypes = (T.POINTER(T.MOTOR_send),)

    c.extract_data.restype = T.c_int
    c.extract_data.argtypes = (T.POINTER(T.MOTOR_recv),)

    c.crc32_core.restype = T.c_uint32
    c.crc32_core.argtypes = (T.POINTER(T.c_uint32), T.c_uint32)

    # 此处需要考虑win64平台和linux平台的区别
    # LSerial.h
    c.open_set.restype = T.c_int
    c.open_set.argtypes = (T.POINTER(T.c_char),)

    c.close_serial.restype = T.c_int
    c.close_serial.argtypes = (T.c_int,)

    # c.broadcast.restype = T.c_int
    # c.broadcast.argtypes(T.c_int, T.POINTER(T.MOTOR_send))

    c.send_recv.restype = T.c_int
    c.send_recv.argtypes = (T.c_int, T.POINTER(T.MOTOR_send), T.POINTER(T.MOTOR_recv))

    return c
