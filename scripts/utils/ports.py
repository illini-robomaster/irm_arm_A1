import os
import platform

def get_port(bytes_=False):
    not_found = 'Cannot open serial: device not attatched.'
    system = platform.system()

    if system == 'Windows':
        port = '\\\\.\\COM3'
    elif system == 'Linux':
        SERIAL_PREFIX = 'usb-FTDI_USB__-__Serial_Converter_'
        dev_basename = '/dev/serial/by-id'
        try:
            path_list = os.listdir(dev_basename)
        except FileNotFoundError as e:  # Nothing connected
            raise RuntimeError(not_found) from e

        dev_paths = (os.path.join(dev_basename, path)
                     for path in path_list
                     if path.startswith(SERIAL_PREFIX))
        try:
            selected_path = next(dev_paths)
        except StopIteration as e:
            raise RuntimeError(not_found) from e

    else:
        raise RuntimeError(f'{system} not supported.')

    return bytes(port, 'utf8') if bytes_ else port
