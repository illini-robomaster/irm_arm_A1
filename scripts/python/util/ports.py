# Illinois RoboMaster 2024
import os
import platform

def get_port(bytes_=False):
    """Searches for possible ports and returns the first one found"""
    NOT_FOUND_MESG = 'Cannot open serial: device not attatched.'
    system = platform.system()

    if system == 'Windows':
        port = '\\\\.\\COM3'
    elif system == 'Linux':
        SERIAL_PREFIX = 'usb-FTDI_USB__-__Serial_Converter_'
        dev_basename = '/dev/serial/by-id'
        try:
            path_list = os.listdir(dev_basename)
        except FileNotFoundError as e:  # Nothing connected
            raise RuntimeError(NOT_FOUND_MESG) from e

        dev_paths = (os.path.join(dev_basename, path)
                     for path in path_list
                     if path.startswith(SERIAL_PREFIX))
        try:
            port = next(dev_paths)
        except StopIteration as e:  # Nothing found
            raise RuntimeError(NOT_FOUND_MESG) from e

    else:
        raise RuntimeError(f'{system} not supported.')

    return bytes(port, 'utf8') if bytes_ else port
