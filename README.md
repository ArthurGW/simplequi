simpleQui v0.10.2
=================

Run codeskulptor.org programs on the desktop using Qt/PySide2

To run an existing codeskulptor script on your local machine, simply import simplequi as simplegui:

    import simplequi as simplegui
    
    # The rest of your script goes here
    
Nothing else should need changing!

Features
--------

- Runs codeskulptor.org Python3 scripts using a Qt application
- The API matches simplegui exactly, so you should be able to run your script exactly as before after importing simplequi

Installation
------------

Get simplequi from pip:

    pip install simplequi
    
Or checkout the source code from https://github.com/ArthurGW/simplequi, then run:

    pip install -r requirements.txt
    
Examples
--------

Included in simplequi/examples are various scripts to show simple usages.

After installing simplequi, these can be run for example like this:

    python -m simplequi.examples.codeskulptor_default
    
Limitations
-----------

- Only supports the simplegui part of the codeskulptor API.  Does not support simplemap, simpleplot or other support 
functions.  Support for simplemap and simpleplot is planned in future.
- Execution happens by the simplequi Qt application running after everything in the script has run, when the python
interpreter is ready to shutdown.  This can cause problems with some debuggers, but is fine for normal use.  Please
report any issues you find with this!
- For now, only supports PySide2/qt-for-python.  Support for PyQt will hopefully be added in future.

Contribute
----------

- Issue Tracker: https://github.com/ArthurGW/simplequi/issues
- Source Code: https://github.com/ArthurGW/simplequi

Support
-------

If you are having issues, please let us know.
The maintainers can be contacted at simplequi.codeskulptor@gmail.com

License
-------

The project is licensed under the GPLv3 license.

**OpenSSL**

The distribution includes a couple of OpenSSL DLLs, which are necessary for getting images and sounds from HTTPS urls.  This
encryption may not be allowed in your country, please check local laws.  These DLLs may only work on Windows, so you
may have to install OpenSSL yourself on other systems.

This product includes software developed by the OpenSSL Project for use in the OpenSSL Toolkit. (http://www.openssl.org/).

See simplequi/resources/ssllib/LICENSE.txt for the full OpenSSL licence details.