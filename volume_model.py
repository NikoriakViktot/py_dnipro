from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

h_values = np.array([
    11, 20.204, 21.041, 21.878, 22.714, 23.551, 24.388, 25.224, 26.061,
    26.898, 27.735, 28.571, 29.408, 30.245, 31.082, 31.918, 32.755, 33.592,
    34.429, 35.265, 36.102, 36.939, 37.776, 38.612, 39.449, 40.286, 41.122,
    41.959, 42.796, 43.633, 44.469, 45.306, 46.143, 46.98, 47.816, 48.653,
    49.49, 50.327, 51.163, 52
])
volumes_thousand_m3 = np.array([
    700000, 803027.4, 815508.6, 828231.3, 841371.9, 855106.3, 869610.5,
    885060.6, 901632.6, 919502.6, 938846.5, 959840.4, 982660.5, 1007483,
    1034478, 1063811, 1095644, 1130139, 1167461, 1207771, 1251232,
    1298008, 1348261, 1402154, 1459850, 1521513, 1587423, 1658030,
    1733798, 1815192, 1902678, 1994913, 2098478, 2221946, 2357548,
    2529488, 2732471, 2955205, 3216346, 3575000
])

# Створюємо DataFrame для збереження даних
reservoir_df = pd.DataFrame({
    'Level (m)': h_values,
    'Volume (thousand m3)': volumes_thousand_m3
})

# Додаємо нульовий рівень з нульовим об'ємом
reservoir_df = pd.concat([pd.DataFrame({'Level (m)': [0], 'Volume (thousand m3)': [0]}), reservoir_df])

# Сортування даних для забезпечення правильної інтерполяції
reservoir_df.sort_values('Level (m)', inplace=True)

# Підгонка поліноміальної кривої до даних
coefficients = np.polyfit(reservoir_df['Level (m)'], reservoir_df['Volume (thousand m3)'], 5)
polynomial = np.poly1d(coefficients)

# Використання поліноміальної функції для генерації значень вздовж всієї кривої
level_range = np.linspace(0, reservoir_df['Level (m)'].max(), 1000)
volume_curve = polynomial(level_range)

# Візуалізація
plt.figure(figsize=(12, 8))
plt.plot(reservoir_df['Level (m)'], reservoir_df['Volume (thousand m3)'], 'o', label='Original Data')
plt.plot(level_range, volume_curve, label='Polynomial Fit Curve')
plt.axhline(0, color='grey', lw=0.7)  # Додаємо лінію x=0 для довідки
plt.title('Volume-Elevation Curve with Zero Volume at Zero Level')
plt.xlabel('Water Level (m)')
plt.ylabel('Reservoir Volume (thousand m³)')
plt.legend()
plt.grid(True)
plt.show()