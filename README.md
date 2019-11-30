# WORK IN PROGRESS

# simpleQui v0.10.0
Run codeskulptor.org programs on the desktop using Qt/PySide2

## Usage
TBW

## Limitations
* Currently, frame.start() enters the main application event loop.
This does not return control to the caller,so this will be the last statement executed in your script.
As long as you keep frame.start() as the very last line in your script, you will be fine.  Hopefully,
this behaviour can be improved in future.

$project
========

$project will solve your problem of where to start with documentation,
by providing a basic explanation of how to do it easily.

Look how easy it is to use:

    import project
    # Get your stuff done
    project.do_stuff()

Features
--------

- Be awesome
- Make things faster

Installation
------------

Install $project by running:

    install project

Contribute
----------

- Issue Tracker: github.com/$project/$project/issues
- Source Code: github.com/$project/$project

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@google-groups.com

License
-------

The project is licensed under the BSD license.