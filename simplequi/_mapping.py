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
from typing import Any, Hashable, Optional


class MappingWithInitCheck(dict):
    """A dict that is only initialised when an item is looked up"""

    def _check_init(self):
        """Check whether self contains any items, if not then initialise"""
        if not len(self):
            self._init_map()

    def _init_map(self):
        raise NotImplementedError("subclasses should implement init map themselves")

    def get(self, key, default=None):
        # type: (Hashable, Optional[Any]) -> Any
        self._check_init()
        return super().get(key, default)

    def __getitem__(self, key):
        # type: (Hashable) -> Any
        self._check_init()
        return super().__getitem__(key)

    def __contains__(self, key):
        # type: (Hashable) -> bool
        self._check_init()
        return super().__contains__(key)
