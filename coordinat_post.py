import pandas as pd
import geopandas as gpd
from pyproj import Proj, transform

# Функція для перетворення координат з формату DMS у десятковий формат
def dms_to_decimal(degrees, minutes, seconds):
    return degrees + minutes / 60 + seconds / 3600

# Дані про пости та координати
data = [
    # ("Prut", "Vorohta", (48, 12, 6.84013), (24, 35, 9.49100), "42249"),
    # ("Prut", "Tatariv", (48, 22, 3.44586), (24, 33, 21.39560), "42136"),
    # ("Prut", "Yaremche", (48, 26, 16.80000), (24, 32, 27.28662), "42137"),
    # ("Prut", "Kolomuia", (48, 31, 23.94459), (25, 0, 59.67962), "42140"),
    # ("Prut", "Chernivci", (48, 18, 42.01021), (25, 54, 56.98081), "42148"),
    # ("Chornuy Cheremosh", "Verhovuna", (48, 9, 15.82490), (24, 50, 11.75796), "42198"),
    # ("Cheremosh", "Ysteriku", (48, 6, 52.89583), (25, 0, 53.05967), "42187"),
    # ("Cheremosh", "Kytu", (48, 15, 0.87447), (25, 10, 53.69206), "42191"),
    # ("Biluy Cheremosh", "Yablunucia", (48, 1, 0.23072), (24, 54, 50.80973), "42194"),
    # ("Ilci", "Ilci", (48.17453301626909,), (24.73373416618596,), "42201"),
    ("Putula", "Putula", (47, 59, 44.67), (25, 5, 7.02), "42202"),
    # ("Chornyava", "Lubkivci", (48.47730216716293,), (25.36204053577276,), "42253"),
]

# Створення списку даних для DataFrame
records = []
for river, name_station, lat_dms, lon_dms, id_station in data:
    if len(lat_dms) == 3:
        lat = dms_to_decimal(*lat_dms)
    else:
        lat = lat_dms[0]
    if len(lon_dms) == 3:
        lon = dms_to_decimal(*lon_dms)
    else:
        lon = lon_dms[0]
    records.append((river, name_station, lat, lon, id_station))

# Створення DataFrame
df = pd.DataFrame(records, columns=["river", "name_station", "latitude", "longitude", "id_station"])

# Перетворення координат у метричні (UTM zone 35N)
proj_utm = Proj(proj='utm', zone=35, ellps='WGS84')
df['easting'], df['northing'] = transform(Proj(init='epsg:4326'), proj_utm, df['longitude'].values, df['latitude'].values)

# Створення GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['easting'], df['northing']), crs="EPSG:32635")

# Збереження у шейп-файл
output_shapefile = "pytula_station_model.shp"

gdf.to_file(output_shapefile)

print(f"Шейп-файл збережено як {output_shapefile}")
