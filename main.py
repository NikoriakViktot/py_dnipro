import geemap
import ee
import fiona
from zipfile import ZipFile
import os

# print(fiona.supported_drivers)
#
# # Розпакування KMZ і знаходження KML файлу
# kmz_path = 'dnipro_down.kmz'
# unzip_folder = kmz_path.replace('.kmz', '')
#
# with ZipFile(kmz_path, 'r') as zip_ref:
#     zip_ref.extractall(unzip_folder)
#
# extracted_files = os.listdir(unzip_folder)
# kml_files = [file for file in extracted_files if file.endswith('.kml')]
#
# for kml_file in kml_files:
#     print(f"Found KML file: {kml_file}")
#     kml_path = os.path.join(unzip_folder, kml_file)  # Оновлений шлях до KML файлу
#     print(f"Full path to KML: {kml_path}")

import json

# Завантаження GeoJSON
with open('dnipro_down.geojson', 'r') as file:
    geojson = json.load(file)

# Видалення третьої координати (висоти) з усіх точок
for feature in geojson['features']:
    if feature['geometry']['type'] == 'LineString':
        feature['geometry']['coordinates'] = [
            [lon, lat] for lon, lat, *_ in feature['geometry']['coordinates']
        ]

# Збереження модифікованого GeoJSON
modified_geojson_path = 'dnipro_down_modified.geojson'
with open(modified_geojson_path, 'w') as file:
    json.dump(geojson, file)

print(f"Modified GeoJSON saved to {modified_geojson_path}")


# Чекайте на завершення завдання експорту через інтерфейс GEE або програмно перевіряючи статус завдання
import ee
import geemap
import json

# Переконайтеся, що ee.Authenticate() викликається лише один раз для аутентифікації.
# ee.Initialize() також потрібно викликати лише один раз після аутентифікації.

# Шлях до модифікованого GeoJSON файлу
modified_geojson_path = 'dnipro_down_modified.geojson'

# Завантаження та модифікація GeoJSON (видалення висоти)
with open(modified_geojson_path, 'r') as file:
    geojson = json.load(file)

for feature in geojson['features']:
    if feature['geometry']['type'] == 'LineString':
        feature['geometry']['coordinates'] = [
            [lon, lat] for lon, lat, *_ in feature['geometry']['coordinates']
        ]

# Завантажуємо модифікований GeoJSON як ee.FeatureCollection
region = geemap.geojson_to_ee(json.dumps(modified_geojson_path))

# Створення буфера навколо лінії
buffer_distance = 5000
region_buffer = region.geometry().buffer(buffer_distance)

# Вибір DEM та кліпування за буферизованою областю
dem = ee.Image("USGS/SRTMGL1_003").clip(region_buffer)

# Визначення параметрів експорту
task = ee.batch.Export.image.toDrive(**{
    'image': dem,
    'description': 'dem_export',
    'folder': 'EarthEngineImages',
    'scale': 30,
    'region': region_buffer.getInfo()['coordinates'],
    'fileFormat': 'GeoTIFF',
})

# Стартування завдання експорту
task.start()

# Чекайте на завершення завдання експорту через інтерфейс GEE або програмно перевіряючи статус завдання
