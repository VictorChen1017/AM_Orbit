# -*- coding: utf-8 -*-
"""LMIO.py Litchi Mission I/O module
---
# Purpose
Read and write the Litchi mission in csv format.
---
# Main objects:
    * LMIO.LitchiWaypoint: Handle the information of each waypoint.
    * LMIO.LitchiMission: Collection of LMIO.LitchiWaypoint and some additional information about the mission.
---
Please write long docstring to describe the objects or methods. A good example is provide by [numpydoc](https://numpydoc.readthedocs.io/en/latest/example.html#example). 
"""

# packages for processing of geospitial data
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point



# test data
flypath = pd.read_csv("C:/Users/USER/Desktop/飛行任務/dont_curved.csv") # test data
# flypath.head()
geometry = [Point(xy) for xy in zip(flypath["longitude"], flypath["latitude"])] # longitude(x), latitude(y) Column name in Litchi csv format
crs = 'EPSG:4326' # default coord system of geometry in Litchi csv
fp = gpd.GeoDataFrame(flypath, geometry=geometry, crs=crs) # create geodataframe
#fp.head() # GeoDataFrame

fp_3826 = fp.to_crs('EPSG:3826') # transform crs using geopandas method, MPP.PY I/O

# extract geometry by list, x and y
fp_3826_x = [point.x for point in fp_3826['geometry']]
fp_3826_y = [point.y for point in fp_3826['geometry']]
print(fp_3826_x)
print(fp_3826_y)

'''
class LitchiWaypoint:
    def __init__(x_coords,y_coords,altitude):
        x_coords = fp_3826_x
        y_coords = fp_3826_y
        altitude = fp_3826["altitude(m)"]
'''