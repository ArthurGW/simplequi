# NOTE: This script is the default script on loading Codeskulptor, included here as a basic smoke test to target dev
# efforts towards.  See https://py3.codeskulptor.org/about.html for details of the creation of Codeskulptor itself,
# including this script.  The copyright in this script is not held by the simplequi creator.

# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor is tested to run in recent versions of
# Chrome, Firefox, and Safari.


import simplequi as simplegui

import math

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
    canvas.draw_text(message, [0, 199], 48, "Red", faces[i])


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 300, 200)
frame.set_canvas_background('aqua')
frame.add_button("Click me", click)
# frame = simplegui.create_frame("Home", 300, 500)
l = frame.add_label('lAB1', 120)
frame.add_input('INPgUT', l.set_text, 300)
frame.set_keydown_handler(lambda x: None)
frame.set_keyup_handler(lambda x: None)
frame.set_mouseclick_handler(lambda x: None)
frame.set_mousedrag_handler(lambda x: None)

calls = 0

def p():
    global calls, t
    calls += 1
    print
    'hello'
    if calls % 10 == 0:
        t.stop()
        print('stop')
        t.start()
        print('start')
        if calls % 30 == 0:
            print('real stop')
            t.stop()

t = simplegui.create_timer(500, p)

t.start()
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
