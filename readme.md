# AtomicMapper Orbit 
Make a terrain-following mission for [Litchi](https://flylitchi.com/) from [atomicMapper](https://cc8.pl/download/atomicmapper.html).  
**Please note that this project is 'In progress'. Any content might change.**
# How to use
(The instructions might change through the development progess.)
1. Make a mission from atomicMapper
2. Prepare the terrain data (e.g. DEM).
3. Run a specific script (not known yet).  
4. Import the modified mission and enjoy.
# Execution enviornment
* Python 3.11+
* gdal (?)

# Development
## Purose
The UAV manufactured by DJI is a powerful tool for mapping. However, the consumer level drone cannot execute a preplanned flight mission. Third party applications like Litchi can control the drone through the [SDK](https://developer.dji.com/cn/mobile-sdk/) and somehow enable the consumer drone to execute flight mission. The [atomicMapper](https://cc8.pl/download/atomicmapper.html) is one of the program which helps to plan the photogrammetry mission for Litchi-supported models.
This tool will modified the mission exported by atomicMapper (in csv format). It will take the every waypoints and compare them with given terrain raster (e.g. DEM in tiff format). All the height will be adjust to achieve the 'terrain-following' mission.
## Developing Phase
### I. Construct Litchi csv IO
Construct the 'waypoint' objects which is compatable to read and write the Litchi csv format.
* `LMIO.py` - The IO module for litchi mission. Two objects, `LitchiWaypoint` and `LitchiMission`, will handle the io of the Litchi CSV format.
### II. Contruct waypoint processing module
Extract the coordinate information from waypoint and use them as the input of DEM extraction. After comparing with the first waypoint, an adjustment value will be add to each waypoint.  
* `MPP.py` - Mission processing module. Including two major tools:
    * `MPP.extractElevationFromDEM()`: Return the elevation value from given coordinate.
    * `MPP.convertToTerrainFollowingMission()`: Import a `LMIO.mission` and a terrain data. modify the elevation of each waypoint to achieve the terrain follwing flight.
    * `MPP.parseCmdArgs()`: The command line parser.
    * `MPP.main()`: Using the command line to execute the program.
---
Please write long docstring to describe the objects or methods. A good example is provide by [numpydoc](https://numpydoc.readthedocs.io/en/latest/example.html#example). More discription will be add in the python file.