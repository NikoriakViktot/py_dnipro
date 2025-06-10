import cdsapi
import geopandas as gpd
import pyproj
import time

# Ініціалізація клієнта CDS API
c = cdsapi.Client(timeout=600, retry_max=50, sleep_max=10)

shapefile_path = ''

# Функція для завантаження даних
def download_era5_data(year, month, variables, bounds, output_file):
    retries = 5  # кількість повторних спроб
    for attempt in range(retries):
        try:
            print(f"Requesting data for {year}-{month:02d} (attempt {attempt + 1}/{retries})")
            c.retrieve(
                'reanalysis-era5-single-levels',
                {
                    'product_type': 'reanalysis',
                    'format': 'netcdf',
                    'variable': variables,
                    'year': str(year),
                    'month': [f'{month:02d}'],
                    'day': [f'{i:02d}' for i in range(1, 32)],
                    'time': [f'{i:02d}:00' for i in range(24)],
                    'area': bounds  # [north, west, south, east]
                },
                output_file
            )
            print(f'Data for {year}-{month:02d} downloaded successfully.')
            break
        except Exception as e:
            print(f"Failed to download data for {year}-{month:02d} on attempt {attempt + 1}/{retries}: {e}")
            time.sleep(120)  # затримка перед повторною спробою
            if attempt == retries - 1:
                print(f"Exceeded maximum retries for {year}-{month:02d}")
                raise


if shapefile_path:
    gdf = gpd.read_file(shapefile_path)
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]

    proj_utm = pyproj.CRS("EPSG:32635")  # UTM Zone 35N
    proj_wgs84 = pyproj.CRS("EPSG:4326")  # WGS84

    transformer = pyproj.Transformer.from_crs(proj_utm, proj_wgs84)

    minx, miny, maxx, maxy = bounds
    min_lon, min_lat = transformer.transform(minx, miny)
    max_lon, max_lat = transformer.transform(maxx, maxy)
    bounds_wgs84 = [max_lat, min_lon, min_lat, max_lon]  # [north, west, south, east]
else:
    bounds_wgs84 = [
        48.1,  # north
        24.8,  # west
        47.9,  # south
        25.3  # east
    ]

print(f"Bounds in WGS84: {bounds_wgs84}")

# Задаємо параметри
years = list(range(1991, 2023 + 1))
variables = [
    'runoff', 'snowmelt', 'evaporation'
]
variable_of_interest = '2m_temperature'

# Завантаження даних за кожен рік і місяць
for year in years:
    for month in range(1, 13):
        output_file = rf"C:\Users\user\PycharmProjects\py_dnipro\pytula\data_pytula\era5_data_snow_NetCDF\era5_data_{year}_{month:02d}.nc"
        try:
            download_era5_data(year, month, variables, bounds_wgs84, output_file)
        except Exception as e:
            print(f"Error downloading data for {year}-{month:02d}: {e}")

