from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from tqdm import tqdm
from constants import CRS
import geopandas as gpd

# https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
BOUNDARY = 'data/cb_2020_us_nation_5m.shp'


def unbounded_voronoi(gdf):
    # GDF must have a geometry that is points
    coords = list(zip(gdf.geometry.x, gdf.geometry.y))

    vor = Voronoi(coords)
    fig = voronoi_plot_2d(vor)
    fig.set_size_inches(25, 15)
    plt.savefig('output/unbounded_voronoi.png')
    plt.show()


def bounded_voronoi(gdf):
    boundary = gpd.read_file('data/cb_2020_us_nation_5m.shp')
    coords = list(zip(gdf.geometry.x, gdf.geometry.y))
    vor = Voronoi(coords)

    r = vor.regions
    r = [i for i in r if -1 not in i]
    r = [i for i in r if len(i) >= 3]

    v = vor.vertices

    p = []
    for reg in r:
        p.append(Polygon([v[i] for i in reg]))

    b = boundary.iloc[0][0]
    p = [i.intersection(b) for i in tqdm(p)]

    g = gpd.GeoSeries(p)
    g.crs = CRS

    fig, ax = plt.subplots()
    boundary.plot(ax=ax, color='grey')
    g.plot(ax=ax, color='grey', edgecolor='orange')
    ax.scatter(gdf.geometry.x, gdf.geometry.y, s=0.5, color='cyan')
    # ax.axis('off')
    plt.xlim([-126, -65])
    plt.ylim([24, 50])
    # plt.axis('equal')
    fig.set_size_inches(25, 10)
    plt.savefig('output/bounded_voronoi')

    plt.show()


def get_regions(gdf):
    boundary = gpd.read_file('data/cb_2020_us_nation_5m.shp')
    coords = list(zip(gdf.geometry.x, gdf.geometry.y))
    vor = Voronoi(coords)

    r = vor.regions
    r = [i for i in r if -1 not in i]
    r = [i for i in r if len(i) >= 3]

    v = vor.vertices

    p = []
    for reg in r:
        p.append(Polygon([v[i] for i in reg]))

    b = boundary.iloc[0][0]
    p = [i.intersection(b) for i in tqdm(p)]

    g = gpd.GeoSeries(p)
    g.crs = CRS

    return g


def get_regions_df(gdf):
    boundary = gpd.read_file('data/cb_2020_us_nation_5m.shp')
    coords = list(zip(gdf.geometry.x, gdf.geometry.y))
    vor = Voronoi(coords)

    r = vor.regions
    r = [i for i in r if -1 not in i]
    r = [i for i in r if len(i) >= 3]

    v = vor.vertices

    p = []
    for reg in r:
        p.append(Polygon([v[i] for i in reg]))

    b = boundary.iloc[0][0]
    p = [i.intersection(b) for i in tqdm(p)]

    g = gpd.GeoSeries(p)
    g.crs = CRS

    return g