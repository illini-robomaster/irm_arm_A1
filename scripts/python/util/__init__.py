# Illinois RoboMaster 2024
import os

from zipfile import ZipFile
from tempfile import TemporaryDirectory

import DISTINFO

from util.motor import Motor
from util.ports import get_port
from util.typedef import Types
from util.libraries import get_so, cdll_bare_init, cdll_init

# Access libraries in zipped context
ZIP_CONTEXT = DISTINFO.DIST

class _ZipContextLibHandler(TemporaryDirectory):
    def __init__(self, zip_path, zipped_path, zip_context):
        if zip_context:
            super().__init__()
            self.zip_path = zip_path
            self.zipped_path = zipped_path
            self.zip_context = zip_context

            self.cwd = os.getcwd()

    def __enter__(self):
        if self.zip_context:
            super().__enter__()
            os.chdir(self.name)
            with ZipFile(self.zip_path) as z:
                z.extract(self.zipped_path, '.')

    def __exit__(self, *args):
        if self.zip_context:
            os.chdir(self.cwd)
            super().__exit__(*args)

so = get_so()

with _ZipContextLibHandler(DISTINFO.ROOT_DIR, so, ZIP_CONTEXT):
    cdll = cdll_init(so)
    cdll_bare = cdll_bare_init(so)

try:
    bport = get_port(bytes_=True)
except:
    bport = None

