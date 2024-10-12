import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline

from scipy.interpolate import interp1d

# Завантажуємо дані з файлу


reservoir_data = pd.read_excel('./volumeDniproSA.xlsx')
# Завантаження даних з наданого файлу Excel

# Перерахування об'єму з км³ в 1000 м³
reservoir_data['w, thousand m3'] = reservoir_data['w, km3'] * 1000000  # Переводимо км³ в тисячі м³

new_range = np.linspace(11, 52, 50)
from scipy.interpolate import interp1d

# Підгонка інтерполяції зі згладжуванням
interp_smooth = interp1d(reservoir_data['h'], reservoir_data['w, thousand m3'], kind='cubic',
                         fill_value=(0.7 * 1000000, reservoir_data['w, thousand m3'].max()),
                         bounds_error=False)

# Отримання значень для нового діапазону
smoothed_values_new_range = interp_smooth(new_range)

# Створення графіку для нового діапазону
plt.figure(figsize=(10, 6))
plt.plot(reservoir_data['h'], reservoir_data['w, thousand m3'], 'o', label='Original Data (thousand m³)')
plt.plot(new_range, smoothed_values_new_range, label='Smoothed Interpolation Curve (thousand m³)', color='green')
plt.title('Cubic Interpolation of Volume Curve from 0.8 km³ to 52m in thousand m³')
plt.xlabel('Level (m)')
plt.ylabel('Volume (thousand m³)')
plt.legend()
plt.grid(True)
plt.show()


# Створення DataFrame для розширених даних із лінійною інтерполяцією у тисячах м³
linear_interpolated_data_thousand = pd.DataFrame({
    'Level (m)': new_range,
    'Volume (thousand m³)': smoothed_values_new_range
})

# Експорт даних до файлу Excel
output_excel_path_thousand = './Interpolated_Reservoir_Volume_Thousand.xlsx'
linear_interpolated_data_thousand.to_excel(output_excel_path_thousand, index=False)

output_excel_path_thousand

