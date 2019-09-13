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
"""Draw some shapes on the canvas and create some control elements"""

import simplequi as simplegui

import math

test = "Font Test"

# Loop counter and font faces to loop through
i = 0
faces = [
    'serif',
    'sans-serif',
    'monospace'
]


# Handler for mouse click
def click():
    global i
    i += 1
    i %= 3


# Handler to draw on canvas
def draw(canvas):
    global i
    canvas.draw_circle([150, 100], 99, 2, 'green', 'purple')
    canvas.draw_line([100, 0], [100, 199], 3, 'red')
    canvas.draw_point([150, 100], 'yellow')
    canvas.draw_point([0, 0], 'red')
    canvas.draw_point([299, 199], 'red')
    canvas.draw_point([299, 0], 'red')
    canvas.draw_point([0, 199], 'red')
    canvas.draw_polyline([(0, 199), (150, 100), (150, 150)], 2, 'green')
    canvas.draw_polygon([(0, 100), (150, 50), (0, 50)], 2, 'green', 'blue')
    canvas.draw_arc([150, 100], 50, 0, math.pi / 2, 2, 'orange')

    # Calculate text size based on fixed width of 150-ish
    width = float('inf')
    size = 72
    while width > 150:
        width = frame.get_canvas_textwidth(test, size, faces[i])
        size -= 1
    canvas.draw_text(test, [0, 199], size, "Red", faces[i])


# Create a frame
frame = simplegui.create_frame("Home", 300, 200)
frame.set_canvas_background('aqua')
frame.add_button("Change Font", click)
lab = frame.add_label('LABEL_TEXT', 120)
frame.add_input('SET LABEL TEXT:', lab.set_text, 200)

# Assign callbacks to event handlers
# Don't actually do anything with these handlers, but they are needed to make the frame display the event parameters
frame.set_keydown_handler(lambda x: None)
frame.set_keyup_handler(lambda x: None)
frame.set_mouseclick_handler(lambda x: None)
frame.set_mousedrag_handler(lambda x: None)

# This one does stuff
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
