import ee
import geemap
import json
ee.Authenticate()
ee.Initialize()

# Шлях до модифікованого GeoJSON файлу
modified_geojson_path = 'dnipro_down_modified.geojson'

# Завантаження модифікованого GeoJSON
with open(modified_geojson_path, 'r') as file:
    geojson = json.load(file)

# Передаємо модифікований GeoJSON об'єкт безпосередньо у geemap.geojson_to_ee
region = geemap.geojson_to_ee(geojson)

buffer_distance = 5000  # 5 км
region_buffer = region.geometry().buffer(buffer_distance)



# Перевірка ініціалізації
print(ee.Image("USGS/SRTMGL1_003").getInfo())


# Вибір DEM та обрізка за буферизованою областю
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

import time

while True:
    status = task.status()
    print(status)
    if status['state'] in ['COMPLETED', 'FAILED']:
        break
    time.sleep(10)  # Зачекайте 10 секунд перед наступною перевіркою статусу

