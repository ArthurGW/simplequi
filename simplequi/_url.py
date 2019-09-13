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

import os
from typing import Callable

from PySide2.QtCore import QByteArray
from PySide2.QtCore import QUrl
from PySide2.QtNetwork import QNetworkRequest, QNetworkReply, QNetworkAccessManager


_MANAGER = QNetworkAccessManager()


def request(url):
    # type: (str) -> QNetworkRequest
    """Construct a network request for the specified url"""
    url = QUrl.fromLocalFile(url) if os.path.isfile(url) else QUrl(url)
    return QNetworkRequest(url)


def request_with_callback(url, callback):
    # type: (str, Callable[[QByteArray], None]) -> QNetworkReply
    """Make a GET request to the given URL and call a callback on finish"""
    req = request(url)
    res = _MANAGER.get(req)
    res.finished.connect(lambda: _on_finished(callback, res))
    return res


def _on_finished(callback, res):
    # type: (Callable[[QByteArray], None], QNetworkReply) -> None
    """Handle the finished request and return the data"""
    res.deleteLater()

    if res.error() == QNetworkReply.NoError:
        data = res.readAll()
        callback(data)
    else:
        raise IOError(res.errorString())
