# -*- coding: utf-8 -*-
"""MPP.py Mission processing module
---
# Purpose
Read and write the Litchi mission in csv format.
---
# Main Tools:
    * `MPP.extractElevationFromDEM()`: Return the elevation value from given coordinate.
    * `MPP.convertToTerrainFollowingMission()`: Import a `LMIO.mission` and a terrain data. modify the elevation of each waypoint to achieve the terrain follwing flight.
    * `MPP.parseCmdArgs()`: The command line parser.
    * `MPP.main()`: Using the command line to execute the program.
---
Please write long docstring to describe the objects or methods. A good example is provide by [numpydoc](https://numpydoc.readthedocs.io/en/latest/example.html#example). 
"""