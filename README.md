# WORK IN PROGRESS

# SimpleQui v0.3.0
Run codeskulptor.org programs on the desktop using Qt/PySide2

## Usage
TBW

## Limitations
* Currently, frame.start() enters the main application event loop.
This does not return control to the caller,so this will be the last statement executed in your script.
As long as you keep frame.start() as the very last line in your script, you will be fine.  Hopefully,
this behaviour can be improved in future.
