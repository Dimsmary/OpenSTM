To run the demo:
Please modify the first line in the script and replace

/opt/bin/lv_micropython

with the path of your micropython binary

The program needs the logging module from micropython-lib which you can install with

upip logging

The image files are loaded with a path relative to the script path. The _images_ directory must therefore be a sub-directory of the path from which demo_printer is run. 
