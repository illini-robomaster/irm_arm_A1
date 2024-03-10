# Illinois RoboMaster 2024
from .ports import get_port
from .typedef import Types
from .libraries import get_so, c_init_bare, c_init

bport = get_port(bytes_=True)

so = get_so()
c = c_init(so)
