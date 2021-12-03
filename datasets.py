# imports
import pandas as pd
import geopandas as gpd
from constants import *
from states import STATES

# constants
ADIP_COLS = [
    'Site Id', 'Facility Type', 'Length', 'State', 'Use', 'Name', 'Loc Id',
    'ARP Latitude', 'ARP Longitude', 'City', 'State Name'
]
ADIP_DATA = 'data/all-airport-data.xlsx'
ADIP_CACHE = 'cache/adip.ftr'


# function to convert FAA lat/longitude to standard
def convert(tude):
    multiplier = 1 if tude[-1] in ['N', 'E'] else -1
    return multiplier * sum(
        float(x) / 60**n for n, x in enumerate(tude[:-1].split('-')))

# get all from airport database
def get_adip():
    # source: FAA ADIP - https://adip.faa.gov/publishedAirports/all-airport-data.xlsx

    df = pd.read_feather(ADIP_CACHE)

    df = df[df['Facility Type'] == 'AIRPORT']
    df = df[df['Length'] >= MIN_RUNWAY_LENGTH]
    df = df[df['State Name'].isin(STATES)]
    df = df[df['Use'] == 'PU']

    geos = df[[
        'Name', 'Loc Id', 'ARP Latitude', 'ARP Longitude', 'City', 'State Name'
    ]].copy()
    geos['Latitude'] = geos['ARP Latitude'].apply(convert)
    geos['Longitude'] = geos['ARP Longitude'].apply(convert)

    gdf = gpd.GeoDataFrame(geos,
                           geometry=gpd.points_from_xy(geos['Longitude'],
                                                       geos['Latitude']))

    gdf.crs = CRS

    return gdf


def cache_adip():
    data = pd.read_excel(ADIP_DATA, sheet_name=None)
    df = pd.merge(left=data['Airports'], right=data['Runways'],
                  on='Site Id')[ADIP_COLS]
    df.to_feather(ADIP_CACHE)