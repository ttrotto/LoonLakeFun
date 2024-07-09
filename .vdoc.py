# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#

#| label: fig-boundaries
#| fig-cap: Malcolm Knapp boundaries and roads.

import numpy as np
import geopandas as gpd
import rasterio as rio
import folium
from folium.plugins import LocateControl
import branca.colormap as cm

# read
boundary = gpd.read_file("data/boundaries.gpkg")
roads = gpd.read_file("data/roads.gpkg")

# styles
def boundary_style(feature):
    return {
        "fillColor": "transparent",
        "color": "white",
        "weight": 2
    }

def roads_style(feature):
    return {
        "color": "yellow",
        "weight": 2
    }

# interactive map
def make_map():
    m = folium.Map(location=[49.30253, -122.56211], zoom_start=12)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Satellite",
        overlay=False
    ).add_to(m)
    folium.GeoJson(data=boundary, style_function=boundary_style).add_to(m)
    folium.GeoJson(data=roads, style_function=roads_style).add_to(m)
    LocateControl().add_to(m)
    return m
make_map()
#
#
#
#
#
#
#
#| label: fig-vector
#| fig-cap: Georeferenced polygons of height and quadratic mean diameter for the Malcolm Knapp research forest. Brighter colors indicate higher values.

# read
poly = gpd.read_file("data/vri2023.gpkg",
                     include_fields = ["QUAD_DIAM_125",
                                       "PROJ_HEIGHT_1",
                                       "VRI_LIVE_STEMS_PER_HA"])
poly.columns = ["diameter", "height", "count", "geometry"]
poly[['height']] /= 100

# styles
colorbars = {
    'diameter': cm.linear.viridis.scale(poly["diameter"].min(), poly["diameter"].max()),
    'height': cm.linear.viridis.scale(poly["height"].min(), poly["height"].max()),
    'count': cm.linear.viridis.scale(poly["count"].min(), poly["count"].max())
}
def styler(feature, property_type):
    values = feature["properties"].get(property_type)
    colorbar = cm.linear.viridis.scale(poly["diameter"].min(), poly["diameter"].max())
    if values is None or np.isnan(values):
        fillColor = "transparent"
    else:
        fillColor = colorbars(values)
    return {
        "fillColor": fillColor,
        "weight": 1,
        "color": "black",
        "opacity": 1,
        "fillOpacity": 1   
    }

# interactive map
def make_map():
    m = folium.Map(location=[49.30253, -122.56211], zoom_start=11.8, tiles=None)
    folium.GeoJson(data=poly[["height", "geometry"]],
        style_function=lambda feature: styler(feature, "height"),
        name="Height"
        ).add_to(m)
    folium.GeoJson(data=poly[["diameter", "geometry"]],
        style_function=lambda feature: styler(feature, "diameter"),
        name="Diameter"
        ).add_to(m)
    folium.GeoJson(data=poly[["count", "geometry"]],
        style_function=lambda feature: styler(feature, "count"),
        name="Stem Count (ha)"
        ).add_to(m)
    folium.LayerControl().add_to(m)
    return m
make_map()
#
#
#
#| label: fig-raster
#| fig-cap: Clipped Landsat 8 scene (RGB 321) above the Malcolm Knapp research forest.

# read
with rio.open("data/landsat.tif") as src:
    landsat = src.read()
    bounds = [*src.bounds]
    bounds = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]

# interactive map
def make_map():
    m = folium.Map(location=[49.30253, -122.56211], zoom_start=12, tiles=None)
    folium.raster_layers.ImageOverlay(
        image='data/landsat.png',
        bounds=bounds
        ).add_to(m)
    return m
make_map()
#
#
#
#
#
#
#
#
#| label: fig-psp
#| fig-cap: Permanent and temporary sample plot locations across southern British Columbia.

# read
psp = gpd.read_file('data/psp.gpkg')['geometry'].to_crs('EPSG:4326')
centroids = [[y, x] for x, y in zip(psp.x, psp.y)] 

# interactive map
def make_map():
    m = folium.Map(location=[49.61253, -122.46211], zoom_start=8, tiles=None)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Satellite",
        overlay=False
    ).add_to(m)
    for point in centroids:
        folium.CircleMarker(location=point,
                            radius=10,
                            fill='white',
                            fill_opacity=0.5
                            ).add_to(m)
    return m
make_map()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| label: fig-comparison
#| fig-cap: Comparison of attributes derived from the VRI polygons
#| fig-subcap: true
#| layout-ncol: 2

import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(poly, x='height', bins=20)
plt.xlabel('Height (m)')
plt.show()

sns.histplot(poly, x='diameter', bins=20)
plt.xlabel('Diameter (cm)')
plt.show()

sns.histplot(poly, x='count', bins=20)
plt.xlabel('Tree count (stems/plot)')
plt.show()
#
#
#
#
#
