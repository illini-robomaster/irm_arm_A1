# Illinois RoboMaster 2024
from util.motor import Motor
from util.ports import get_port
from util.typedef import Types
from util.libman import get_so_path, cdll_bare_init, cdll_init

so_path = get_so_path()

cdll = cdll_init(so_path)
cdll_bare = cdll_bare_init(so_path)

try:
    bport = get_port(bytes_=True)
except:
    bport = None
