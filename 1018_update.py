# extract method

# I/O : Input 3826 list of x, y such that
# x = [305204.723173963022418,305220.630195463774726, ....]
# y = [2782586.360826591961086, 2782576.093745744321495, ...]
# raster path 

# import

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

from osgeo import gdal


import sys
import numpy as np



# input data
path = "C:/Users/USER/Documents/GIS圖資/常用基本圖資/Raster/台北DEM/taipei dem3826.tif"
fly_path = "C:/Users/USER/Desktop/飛行任務/dont_curved.csv"
output_path = "C:/Users/USER/Downloads/flypath.csv" #輸出路徑

#x_coords = [305283.946661491296254,305220.6301954637]
#y_coords = [2782556.027021550107747,2782576.09374574]

flypath = pd.read_csv(fly_path)
geometry = [Point(xy) for xy in zip(flypath["longitude"], flypath["latitude"])] # longitude(x), latitude(y) Column name in Litchi csv format
crs = 'EPSG:4326' # default coord system of geometry in Litchi csv
fp = gpd.GeoDataFrame(flypath, geometry=geometry, crs=crs) # create geodataframe
#fp.head() # GeoDataFrame
fp_3826 = fp.to_crs('EPSG:3826') # transform crs using geopandas method, MPP.PY I/O

fp_3826_x = [point.x for point in fp_3826['geometry']]
fp_3826_y = [point.y for point in fp_3826['geometry']]
#print(fp_3826_x)
#print(fp_3826_y)


x_coords = fp_3826_x
y_coords = fp_3826_y

# extract method

def extract(path:str,x_coords:list[float],y_coords:list[float])->list[float|int]:
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

# main 
result = extract(path,x_coords,y_coords)

base_hight = result[0]
delta_hight = result
for i in range(0,len(delta_hight)):
    delta_hight[i] = result[i]-base_hight
# print(delta_hight) # difference between orignal hight dem and way pts

flypath["new_elev"] = flypath["altitude(m)"]+delta_hight # edit heights
#print(flypath["new_elev"])
flypath.to_csv(output_path, index=True)