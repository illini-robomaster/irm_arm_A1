# Everything before
# %DIST%
# will be removed in `distribute.sh` output.
import os.path

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
DIST = False#%DIST%DIST = True
