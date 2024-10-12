import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Шлях до файлу
data_flow = r"C:\Users\user\PycharmProjects\py_dnipro\pytula\daily_avg_flow.csv"

# Завантаження даних з вказівкою назв колонок та парсингом дат
data = pd.read_csv(data_flow, parse_dates=['Дата'], index_col='Дата', names=['Дата', 'Runoff'], header=0)

# Вибірка даних за конкретні роки
years_to_analyze = [2006, 2007, 2008,2009,2010]
k_values = []
ratios_to_peak = []

for year in years_to_analyze:
    # Вибірка даних за рік
    yearly_data = data[data.index.year == year]

    # Підгонка лінійної трендової лінії (логарифмічна модель)
    log_runoff = np.log(yearly_data['Runoff'])
    days = (yearly_data.index - yearly_data.index.min()).days
    slope, intercept = np.polyfit(days, log_runoff, 1)

    # Визначення константи спаду
    k = -slope
    k_values.append(k)

    # Розрахунок співвідношення до пікового витоку
    ratio_to_peak = yearly_data['Runoff'].min() / yearly_data['Runoff'].max()
    ratios_to_peak.append(ratio_to_peak)

    # Графік логарифмічного витоку та трендової лінії
    plt.figure(figsize=(10, 5))
    plt.scatter(days, log_runoff, label='Log of Runoff')
    plt.plot(days, slope * days + intercept, 'r-', label=f'Fit: ln(Q) = {slope:.5f}t + {intercept:.5f}')
    plt.title(f'Log of Runoff for {year}')
    plt.xlabel('Days from start of year')
    plt.ylabel('Log of Runoff')
    plt.legend()
    plt.grid(True)
    plt.show()

# Обрахунок середніх значень
average_k = np.mean(k_values)
average_ratio = np.mean(ratios_to_peak)

print(f"Average Recession Constant (K) over years: {average_k:.5f}")
print(f"Average Ratio to Peak over years: {average_ratio:.5f}")

# Ініціальний виток
initial_discharge = data.loc['2003-01-01', 'Runoff']
print(f"Initial Discharge on January 1, 2003: {initial_discharge} m³/s")
