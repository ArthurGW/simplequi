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

from PySide2.QtMultimedia import QAudio, QMediaPlayer, QMediaContent

from ._app import TheApp
from ._url import request


class Sound:
    def __init__(self, url):
        # type: (str) -> None
        """
        Loads a sound from the specified URL.

        Supports whatever audio formats that PySide2 supports (depending on locally-installed codecs).
        No error is raised if the file isn't found or is of an unsupported format.
        """
        req = request(url)
        content = QMediaContent(req)
        self.__player = QMediaPlayer(flags=QMediaPlayer.LowLatency)
        self.__player.setAudioRole(QAudio.GameRole)
        self.__player.setMedia(content)
        self.__player.mediaStatusChanged.connect(self.__on_status_changed)
        self.__player.error.connect(self.__on_status_changed)
        TheApp.add_tracked(self)
        self.__sound_loaded = False
        self.__play_requested = False

    def __on_status_changed(self, _):
        # type: (QMediaPlayer.MediaStatus) -> None
        """Check if the sound is loaded"""
        error = self.__player.error()
        status = self.__player.mediaStatus()
        if error == QMediaPlayer.NoError and QMediaPlayer.LoadedMedia <= status < QMediaPlayer.InvalidMedia:
            self.__sound_loaded = True
            if self.__play_requested and status != QMediaPlayer.EndOfMedia:
                return self.play()
        else:
            self.__sound_loaded = False
        self.__play_requested = False
        TheApp.remove_tracked(self)

    def play(self):
        """Starts playing a sound, or restarts playing it at the point it was paused"""
        if self.__sound_loaded:
            self.__player.play()
            TheApp.add_tracked(self)
        self.__play_requested = True

    def pause(self):
        """Stops the playing of the sound. Playing can be restarted at the stopped point with Sound.play()"""
        if self.__sound_loaded:
            self.__player.pause()
            TheApp.remove_tracked(self)
        self.__play_requested = False

    def rewind(self):
        """Stops playing the sound, and makes it so the next play() will start playing the sound at the beginning"""
        if self.__sound_loaded:
            self.__player.stop()
            TheApp.remove_tracked(self)
        self.__play_requested = False

    def set_volume(self, volume):
        # type: (float) -> None
        """Changes the volume for the sound to be the given level on a 0 (silent)–1.0 (maximum) scale. Default is 1."""
        assert 0.0 <= volume <= 1.0, "volume must be given in range 0-1 inclusive"
        self.__player.setVolume(int(100 * volume))
