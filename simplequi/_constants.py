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
"""A few simple constants that are used in multiple other modules"""

from typing import Tuple

from PySide2.QtCore import QMargins

# Widget layouts
DEFAULT_WIDGET_HEIGHT = 25  #: Default height mostly for frame control area widgets
DEFAULT_CONTROL_ENTRY_WIDTH = 200  #: Default width for controls
DEFAULT_FRAME_MARGIN = QMargins(*([20]*4))  #: Default widget-free margin around the edges of the frame
NO_MARGINS = QMargins()  #: No margin on any side

# Types
Point = Tuple[int, int]  #: Used for specifying coordinates
Size = Point  #: Used for specifying width & height pairs
