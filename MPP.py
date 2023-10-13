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

from osgeo import gdal
# from osgeo import ogr
# from osgeo import osr
# from osgeo import gdal_array
# from osgeo import gdalconst
# import numpy as np
import sys




def extractElevationFromDEM(path:str,x_coords:list[float],y_coords:list[float])->list[float|int]:
    '''
    this methon can sample the values from DEM for given points.
    
    Parameters:
    -----
    path:str path of DEM dataset
    x_coords:list[float] x_coordinates of points
    y_coords:list[float] y_coordinates of points

    Output
    -----
    elev:list[float|int] list of elevation extract results
    
    Reference
    -----
    https://gis.stackexchange.com/questions/225370/get-individual-pixel-values-on-a-raster-image-using-gdal-and-python
    https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html#get-raster-band

    '''
    # this allows GDAL to throw Python Exceptions
    gdal.UseExceptions()
    try:
        src_ds = gdal.Open(path)
    except RuntimeError as e:
        print('Unable to open INPUT.tif')
        print(e)
        sys.exit(1)

    try:
        band = src_ds.GetRasterBand(1)
    except RuntimeError as e:
        # for example, try GetRasterBand(10)
        print(e)
        sys.exit(1)

    geotransform = src_ds.GetGeoTransform() # (296110.0, 20.0, 0.0, 2789170.0, 0.0, -20.0) top left x, pixel size , rotation,  top left y, pixel size , rotation
    band = src_ds.GetRasterBand(1)
    xOrigin = geotransform[0]
    yOrigin = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]

    elev = [] # storage elevation result

    for i in range(len(x_coords)): # number of data
        x = x_coords[i]
        y = y_coords[i]
        # compute pixel offset
        xOffset = int((x - xOrigin) / pixelWidth)
        yOffset = int((y - yOrigin) / pixelHeight)
        # get individual pixel values
        data = band.ReadAsArray(xOffset, yOffset, 1, 1)
        value = data[0, 0]
        elev.append(value)

    return elev

def convertToTerrainFollowingMission(elev,extractElevationFromDEM):
    base_hight = elev[0]
    delta_hight = elev
    for i in range(0,len(delta_hight)):
        delta_hight[i] = elev[i]-base_hight # calculate difference between orignal hight dem and way pts
    
    return delta_hight

