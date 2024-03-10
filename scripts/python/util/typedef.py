<<<<<<<< HEAD:scripts/python/util/typedef.py
========
import os
import sys

>>>>>>>> 8755b0f (Refactor and package):scripts/utils/typedef.py
from ctypes import *

class COMData32(Union):
    _fields_ = [("L", c_int32), ("u8", c_uint8*4), ("u16", c_uint16*2), ("u32", c_uint32), ("F", c_float)]

class COMHead(Structure):
    _fields_ = [("start", c_ubyte*2), ("motorID", c_ubyte), ("reserved", c_ubyte)]

class MasterComdV3(Structure):
    _pack_ = 1
    # _fields_ = [("mode", c_uint8)]
    _fields_ = [("mode", c_uint8), ("ModifyBit", c_uint8), ("ReadBit", c_uint8), \
        ("reserved", c_uint8), ("Modify", COMData32), ("T", c_int16), \
        ("W", c_int16), ("Pos", c_int32), ("K_P", c_int16), ("K_W", c_int16), \
        ("LowHzMotorCmdIndex", c_uint8), ("LowHzMotorCmdByte", c_uint8), \
        ("Res", COMData32)]


class MasterComdDataV3(Structure):
    _pack_ = 1
    _fields_ = [("head", COMHead), ("Mdata", MasterComdV3), ("CRCdata", COMData32)]

class ServoComdV3(Structure):
    _pack_ = 1
    _fields_ = [("mode", c_uint8), ("ReadBit", c_uint8), ("Temp", c_int8), \
        ("MError", c_uint8), ("Read", COMData32), ("T", c_int16), ("W", c_int16), \
        ("LW", c_float), ("W2", c_int16), ("LW2", c_float), ("Acc", c_int16), \
        ("OutAcc", c_int16), ("Pos", c_int32), ("Pos2", c_int32), \
        ("gyro", c_int16*3), ("acc", c_int16*3), ("Fgyro", c_int16*3), ("Facc", c_int16*3), \
        ("Fmag", c_int16*3), ("Ftemp", c_uint8), ("Force16", c_int16), \
        ("Force8", c_int8), ("FError", c_uint8), ("Res", c_int8)]


class ServoComdDataV3(Structure):
    _pack_ = 1
    _fields_ = [("head", COMHead), ("Mdata", ServoComdV3), ("CRCdata", COMData32)]

class MOTOR_send(Structure):
    _fields_ = [("motor_send_data", MasterComdDataV3), ("hex_len", c_int), \
        ("send_time", c_longlong), ("id", c_ushort), ("mode", c_ushort), \
        ("T", c_float), ("W", c_float), ("Pos", c_float), ("K_P", c_float), ("K_W", c_float)]

class MOTOR_recv(Structure):
    _fields_ = [("motor_recv_data", ServoComdDataV3), ("hex_len", c_int), \
        ("recv_time", c_longlong), ("correct", c_int), ("motor_id", c_ubyte), \
        ("mode", c_ubyte), ("Temp", c_int), ("MError", c_ubyte), \
        ("T", c_float), ("W", c_float), ("LW", c_float), ("Acc", c_int), \
        ("Pos", c_float), ("gyro", c_float*3), ("acc", c_float*3)]

class Types:
    COMData32 = COMData32
    COMHead = COMHead
    MasterComdDataV3 = MasterComdDataV3
    ServoComdV3 = ServoComdV3
    ServoComdDataV3 = ServoComdDataV3
    MOTOR_send = MOTOR_send
    MOTOR_recv = MOTOR_recv
    Union = Union
    Structure = Structure
    POINTER = POINTER
    byref = byref
    c_int = c_int
    c_int8 = c_int8
    c_uint8 = c_uint8
    c_int16 = c_int16
    c_uint16 = c_uint16
    c_int32 = c_int32
    c_uint32 = c_uint32
    c_float = c_float
    c_char = c_char
    c_ubyte = c_ubyte
    c_longlong = c_longlong
    c_ushort = c_ushort
<<<<<<<< HEAD:scripts/python/util/typedef.py
    cdll = cdll
========
>>>>>>>> 8755b0f (Refactor and package):scripts/utils/typedef.py
