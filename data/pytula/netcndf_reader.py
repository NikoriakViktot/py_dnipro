import pandas as pd
from netCDF4 import Dataset
import os

# Задаємо параметри
years = list(range(1991, 2023 + 1))
variables = [
    '2m_temperature', 'total_precipitation'
]
variable_map = {
    '2m_temperature': 't2m',
    'total_precipitation': 'tp'
}

# Функція для обробки даних NetCDF та збереження у форматі DataFrame
def process_netcdf_to_df(netcdf_file, variable):
    dataset = Dataset(netcdf_file)

    # Перевірка наявності змінної у файлі
    if variable not in dataset.variables:
        print(f"Змінної '{variable}' немає у файлі {netcdf_file}")
        return pd.DataFrame()

    data = dataset.variables[variable][:]
    times = dataset.variables['time'][:]
    latitudes = dataset.variables['latitude'][:]
    longitudes = dataset.variables['longitude'][:]

    time_index = pd.to_datetime(times, unit='h', origin='1900-01-01')

    df_list = []
    for i, lat in enumerate(latitudes):
        for j, lon in enumerate(longitudes):
            temp_df = pd.DataFrame(data[:, i, j], index=time_index, columns=[f'{variable}_{lat}_{lon}'])
            df_list.append(temp_df)

    df = pd.concat(df_list, axis=1)
    return df

# Об'єднання всіх щомісячних даних в один датафрейм для кожної змінної
all_data_dfs = {var: pd.DataFrame() for var in variable_map.values()}

for year in years:
    for month in range(1, 13):
        netcdf_file = rf"C:\Users\user\PycharmProjects\py_dnipro\pytula\data_pytula\era5_data_NetCDF\era5_data_{year}_{month:02d}.nc"
        for variable in variable_map.values():
            month_df = process_netcdf_to_df(netcdf_file, variable)
            if not month_df.empty:
                all_data_dfs[variable] = pd.concat([all_data_dfs[variable], month_df])

# Обчислення добової суми опадів і середньої температури за день після обчислення середнього значення для трьох координат
daily_data_dfs = {}
for variable, df in all_data_dfs.items():
    if not df.empty:
        if variable == 'tp':
            # Середнє значення між трьома різними даними для координат, потім сума опадів за день
            df_mean = df.mean(axis=1)
            daily_data_dfs[variable] = df_mean.resample('D').sum()
        else:
            # Середнє значення між трьома різними даними для координат, потім середнє значення температури за день
            df_mean = df.mean(axis=1)
            daily_data_dfs[variable] = df_mean.resample('D').mean()

# Перетворення даних опадів з метрик у міліметри і температури з Кельвінів у Цельсії
if 'tp' in daily_data_dfs:
    daily_data_dfs['tp'] *= 1000  # Перетворення з метрик в міліметри
    daily_data_dfs['tp'][daily_data_dfs['tp'] < 0] = 0  # Забезпечення того, що суми опадів не є від'ємними

if 't2m' in daily_data_dfs:
    daily_data_dfs['t2m'] -= 273.15  # Перетворення з Кельвінів у Цельсії

# Обчислення середнього значення для всього басейну і заокруглення до 2 знаків після коми
for variable, df in daily_data_dfs.items():
    daily_data_dfs[variable] = df.round(2)

# Збереження даних у форматі CSV без заголовку стовпця
output_dir = r"C:\Users\user\PycharmProjects\py_dnipro\pytula\data_pytula\data_csv"
os.makedirs(output_dir, exist_ok=True)

for variable, df in daily_data_dfs.items():
    output_csv = os.path.join(output_dir, f"era5_{variable}_daily.csv")
    df.to_csv(output_csv, header=False)
    print(f'Data for {variable} processed and saved to CSV successfully.')
