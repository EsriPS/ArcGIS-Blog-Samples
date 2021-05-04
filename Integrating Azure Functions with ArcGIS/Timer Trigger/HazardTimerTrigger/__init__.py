import datetime
import logging
import azure.functions as func
import json
import logging
import os
import pandas as pd
import sys
import time
from arcgis.gis import GIS
from arcgis.features import SpatialDataFrame
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from arcgis.geometry import buffer, intersect
from arcgis.geometry.filters import intersects
from datetime import datetime, timedelta


def main(mytimer: func.TimerRequest) -> None:

    # Get Start Time
    start_time = time.time()

    # Get Connection Parameters
    agol_url = os.environ['agol_org']
    agol_username = os.environ['agol_username']
    agol_password = os.environ['agol_password']

    # Get Configuration File
    this_dir = os.path.split(os.path.realpath(__file__))[0]
    config_file = os.path.join(this_dir, 'config.json')
    params = get_config(config_file)
    layers = params['layers']
    usa_geom = params['usa_geom']

    # Get GIS Object
    gis = GIS(agol_url, agol_username, agol_password)
    logging.info('Generated GIS object')
    
    #### INSERT CODE HERE WORKING WITH GIS OBJECT ####


def get_config(in_file):
    with open(in_file) as config:
        param_dict = json.load(config)

    return param_dict
