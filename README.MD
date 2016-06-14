NOAA Weather Radar for Alfred
=============================

This is an Alfred Workflow that downloads the latest weather radar images from NOAA, compiles them into an animated gif, and displays this gif with Quicklook. It's written in python and runs reasonably fast but future versions may be faster. It should notify of updates automatically, checking for updates on standard invocation if it hasn't checked in 7 days and provides an option to intall said update automatically should it exist.

Please note that many functions provided by the JSON library and urllib I use are replacable by internal functions to the Alfred-Workflow python library by Dean Jackson that I'm already using so I'll probably prone those libraries soon. I also have a plan to dramatically increase the speed of the initial display to near instantaneous (order 1/4 second) by predownloading the static images before enter is pressed on the standard radar query. This will require a little more experimentation with the subprocess module as I need to see if subprocesses are still running or not for this to work.

[more to come here]