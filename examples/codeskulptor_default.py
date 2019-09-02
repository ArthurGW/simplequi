# NOTE: This script is the default script on loading Codeskulptor, included here as a basic smoke test to target dev
# efforts towards.  See https://py3.codeskulptor.org/about.html for details of the creation of Codeskulptor itself,
# including this script.  The copyright in this script is not held by the simplequi creator.

# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor is tested to run in recent versions of
# Chrome, Firefox, and Safari.


import simplequi as simplegui
import math

from _canvas import Canvas

message = "Welcome!"

faces = [
    'serif',
    'sans-serif',
    'monospace'
]

i = 0
# Handler for mouse click
def click(v=None):
    global message, i
    message = "Good job!"
    i += 1
    i %= 3


# Handler to draw on canvas
def draw(canvas):
    # type: (Canvas) -> None
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
    canvas.draw_text(message, [50,112], 48, "Red", faces[i])


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 300, 200)
frame.set_canvas_background('aqua')
frame.add_button("Click me", click)
l = frame.add_label('lAB1', 120)
frame.add_input('INPgUT', l.set_text, 300)

frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
