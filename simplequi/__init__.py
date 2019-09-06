# -----------------------------------------------------------------------------
# Copyright ©2019 Arthur Gordon-Wright
# <https://github.com/ArthurGW/simplequi>
# <simplequi.codeskulptor@gmail.com>
#
# This file is part of simplequi.
#
# simplequi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# simplequi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with simplequi.  If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
__imported = False

if not __imported:
    __imported = True
    import _api
    from _api import *

    __all__ = _api.__all__
    __version__ = '0.4.1'

    import os
    import sys
    import subprocess
    orig = sys.modules['__main__'].__file__
    bootstrap = os.path.join(os.path.dirname(__file__), '_bootstrap.py')
    if orig != bootstrap:
        proc = subprocess.Popen([sys.executable, bootstrap, orig])
        proc.wait()
        sys.exit(0)
    # with open(orig, 'r') as f:
    #     script = f.readlines()

    # sc_ = 'def scr_():\n'
    # for l in script:
    #     sc_ += '    ' + l + '\n'
    # sc_ += 'QTimer.singleShot(100, scr_)\n'
    # sc_ += 'TheApp.exec_()\nimport time\ntime.sleep(5)\n'
    # exec(sc_)

