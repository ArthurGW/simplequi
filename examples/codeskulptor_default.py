# NOTE: This script is the default script on loading Codeskulptor, included here as a basic smoke test to target dev
# efforts towards.  See https://py3.codeskulptor.org/about.html for details of the creation of Codeskulptor itself,
# including this script.  The copyright in this script is not held by the simplequi creator.

# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor is tested to run in recent versions of
# Chrome, Firefox, and Safari.


import simplequi as simplegui

message = "Welcome!"


# Handler for mouse click
def click(v=None):
    global message
    message = "Good job!"


# Handler to draw on canvas
def draw(canvas):
    # canvas.draw_text(message, [50,112], 48, "Red")
    pass


# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 300, 200)
frame.set_canvas_background('aqua')
frame.add_button("Click me", click)
l = frame.add_label('lAB1', 120)
frame.add_input('INPgUT', l.set_text, 300)

frame.set_draw_handler(draw)

# Start the frame animation
frame.start()
