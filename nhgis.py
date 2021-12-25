# file to read input data from NHGIS
from constants import CRS
import pandas as pd
import geopandas as gpd

# demos filepath
DEMOS_PATH = 'data/nhgis/demos/tract/nhgis0002_ds248_2020_tract.csv'

# GIS directory
GIS_PATH = 'data/nhgis/gis/tract/US_tract_2020.shp'

# encoding
ENCODING = 'iso-8859-1'

# GIS key
KEY = 'GISJOIN'

# Population Column from Source Data
POP_SOURCE = 'U7B001'

# Population Column in Output File
POP_OUT = 'POP'

# Geometry columnn
GEOM = 'geometry'

# Output Path
OUT_PATH = 'cache/nhgis/merged/tract'


def get_tracts():
    # read in tract shapefiles and create geodataframe
    geos = gpd.read_file(GIS_PATH).set_index(KEY)[[GEOM]]

    # read in tract populations and create series
    pops = pd.read_csv(DEMOS_PATH,
                       usecols=[KEY, POP_SOURCE],
                       low_memory=True,
                       encoding=ENCODING).set_index(KEY)[POP_SOURCE]

    # rename series
    pops.name = POP_OUT

    # merged geos and pops
    merged = geos.merge(pops, on=KEY)

    # set CRS
    merged.crs = CRS

    return merged


def save_tracts():
    merged = get_tracts()

    # output shapefiles with populations
    merged.to_file(OUT_PATH)