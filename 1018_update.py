# -*- coding: utf-8 -*-
""" 1018_update
A functional script to add the terrain information to litchi flight route.
'###' is the comment indicates the future modularization work.
"""
# import

# built in
import sys
import numpy as np
from pathlib import Path
import argparse
# 3rd party
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

from osgeo import gdal
### The 'extract' could merge to 'MPP.extractElevationFromDEM' 
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
        src_ds = gdal.Open(str(path))
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

def main(demPath:Path,missionPath:Path,outputPath:Path)->None:
    """
    """
    ### Create and merge the following script to method 'LMIO.LitchiMission.read()'
    flypath = pd.read_csv(missionPath) 
    
    ### Create and merge the following script to attribute 'LMIO.LitchiMission.WaypointsXY'
    geometry = [Point(xy) for xy in zip(flypath["longitude"], flypath["latitude"])] # longitude(x), latitude(y) Column name in Litchi csv format
    
    ### Create and merge the following script to method 'LMIO.LitchiMission.returnXYCoordinateInCrs()'
    crs = 'EPSG:4326' # default coord system of geometry in Litchi csv
    fp = gpd.GeoDataFrame(flypath, geometry=geometry, crs=crs) # create geodataframe
    fp_3826 = fp.to_crs('EPSG:3826') # transform crs using geopandas method, MPP.PY I/O
    fp_3826_x = [point.x for point in fp_3826['geometry']]
    fp_3826_y = [point.y for point in fp_3826['geometry']]
    x_coords = fp_3826_x
    y_coords = fp_3826_y
    
    ### Merge the following script to method 'MPP.convertToTerrainFollowingMission()' 
    result = extract(demPath,x_coords,y_coords)
    base_hight = result[0]
    delta_hight = result
    for i in range(0,len(delta_hight)):
        delta_hight[i] = result[i]-base_hight
    # print(delta_hight) # difference between orignal hight dem and way pts
    flypath["new_elev"] = flypath["altitude(m)"]+delta_hight # edit heights
    #print(flypath["new_elev"])
    ### Create and merge the following script to method 'LMIO.LitchiMission.save()'
    flypath.to_csv(outputPath, index=True)


def main_inline()->None:
    """Execute the script inline. Read a
    How to use: 
    *   Modify the file route."""

    # input data
    demPath = Path(r"C:\Users\USER\Documents\GIS圖資\常用基本圖資\Raster\台北DEM\taipei dem3826.tif")
    flyPath = Path(r"C:\Users\USER\Desktop\飛行任務\dont_curved.csv")
    outputPath = Path(r"C:\Users\USER\Downloads\flypath.csv") #輸出路徑

    # execute
    main(demPath=demPath,missionPath=flyPath,outputPath=outputPath)

def parseCommandArgs()->argparse.Namespace:
    """ Parse the command line arguments using argparse
    用途：定義並且處理命令列參數。
    命令列傳入文法：
        `python ./1018_update.py DEM_Path FlyPath OutputPath`
    此處僅有位置變數（跟傳入順序有關）而沒有選擇參數（和參數的前綴名稱有關如「-h」，而與位置無關），目前程式已經新增「DEM」變數，可如法炮製另外兩個變數。
    
    新增參數的方法請參考:
    https://docs.python.org/3/howto/argparse.html

    """
    parser = argparse.ArgumentParser(description='this is a description')
    parser.add_argument('DEM',action='store',type=Path,help='The DEM path.')
    parser.add_argument('FlyRoute',action='store',type=Path,help='The FlyRoute path.')
    parser.add_argument('outputPath',action='store',type=Path,help='The output path.')
    return parser.parse_args()

def main_cmd():
    """ main in command line mode
    讀取命令列輸入的變數
    """
    args:argparse.Namespace = parseCommandArgs()
    #print(args.DEM,args.FlyRoute,args.outputPath)
    main(args.DEM,args.FlyRoute,args.outputPath)


if __name__ == '__main__':
    ## command line mode
    main_cmd()
    ## in-line mode
    #main_inline()