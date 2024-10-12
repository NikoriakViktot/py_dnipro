import pandas as pd
import os

# Налаштуйте опції для відображення більшої кількості рядків
pd.set_option('display.max_rows', None)  # Відображення всіх рядків
pd.set_option('display.max_columns', None)  # Відображення всіх стовпців
pd.set_option('display.width', None)  # Автоматичне розширення ширини консолі
pd.set_option('display.max_colwidth', None)  # Показувати повний текст у стовпцях


# Шлях до папки з файлами
folder_path = r"C:\Users\user\PycharmProjects\py_dnipro\datа_post"
output_folder = os.path.join(folder_path, 'results')
os.makedirs(output_folder, exist_ok=True)
# Обробка кожного файлу в папці
for filename in os.listdir(folder_path):
    if filename.endswith(".xls") or filename.endswith(".xlsx"):
        file_path = os.path.join(folder_path, filename)

        # Завантаження даних з файлу
        df = pd.read_excel(file_path)

        # Виведіть назви стовпців для перевірки
        print(f"Columns in file {filename}: {df.columns}")

        # Переконайтесь, що всі стовпці дат і часу є строками
        for col in ['Дата ', 'Час', 'Дата .1', 'Час.1', 'Дата .2', 'Час.2', 'Дата .3', 'Час.3']:
            if col in df.columns:
                df[col] = df[col].astype(str)

        # Об'єднання дати і часу в один стовпець datetime для кожного параметру
        if 'Дата .1' in df.columns and 'Час.1' in df.columns:
            df['datetime'] = pd.to_datetime(df['Дата .1'] + ' ' + df['Час.1'], errors='coerce', dayfirst=True)
        if 'Дата ' in df.columns and 'Час' in df.columns:
            df['datetime_level'] = pd.to_datetime(df['Дата '] + ' ' + df['Час'], errors='coerce', dayfirst=True)
            print(f"datetime_level created: {df['datetime_level'].head()}")
        if 'Дата .2' in df.columns and 'Час.2' in df.columns:
            df['datetime_precip'] = pd.to_datetime(df['Дата .2'] + ' ' + df['Час.2'], errors='coerce', dayfirst=True)
            print(f"datetime_precip created: {df['datetime_precip'].head()}")
        if 'Дата .3' in df.columns and 'Час.3' in df.columns:
            df['datetime_temp'] = pd.to_datetime(df['Дата .3'] + ' ' + df['Час.3'], errors='coerce', dayfirst=True)
            print(f"datetime_temp created: {df['datetime_temp'].head()}")

        # Ім'я файлу без розширення
        file_base = os.path.splitext(filename)[0]

        # Обчислення середніх значень і сумарних значень
        if 'datetime_flow' in df.columns and 'Витрата, м³/с' in df.columns:
            df_daily_avg = df.groupby(df['datetime'].dt.date)['Витрата, м³/с'].mean().reset_index()
            df_daily_avg.columns = ['Дата', 'Середня витрата, м³/с']
            df_daily_avg.to_csv(os.path.join(output_folder, f'{file_base}_daily_avg_flow.csv'), index=False, float_format='%.3f')

            print(f"Saved {file_base}_daily_avg_flow.csv")

        if 'datetime_level' in df.columns and 'Рівень (без зрізки), см' in df.columns:
            daily_avg_level = df.groupby(df['datetime_level'].dt.date)['Рівень (без зрізки), см'].mean().reset_index()
            daily_avg_level.columns = ['Дата', 'Середній рівень, см']
            daily_avg_level['Середній рівень, см'] = daily_avg_level['Середній рівень, см'].astype(int)
            daily_avg_level.to_csv(os.path.join(output_folder, f'{file_base}_daily_avg_level.csv'), index=False,
                                   header=False)
            print(f"Saved {file_base}_daily_avg_level.csv")

        if 'datetime_precip' in df.columns and 'Опади, мм' in df.columns:
            daily_sum_precipitation = df.groupby(df['datetime_precip'].dt.date)['Опади, мм'].sum().reset_index()
            daily_sum_precipitation.columns = ['Дата', 'Сумарні опади, мм']
            daily_sum_precipitation.to_csv(os.path.join(output_folder, f'{file_base}_daily_sum_precipitation.csv'),
                                           index=False, header=False, float_format='%.1f')
            print(f"Saved {file_base}_daily_sum_precipitation.csv")

        if 'datetime_temp' in df.columns and 'Температура повітря,ºС' in df.columns:
            daily_avg_temperature = df.groupby(df['datetime_temp'].dt.date)[
                'Температура повітря,ºС'].mean().reset_index()
            daily_avg_temperature.columns = ['Дата', 'Середня температура, ºС']
            daily_avg_temperature.to_csv(os.path.join(output_folder, f'{file_base}_daily_avg_temperature.csv'),
                                         index=False, header=False, float_format='%.1f')
            print(f"Saved {file_base}_daily_avg_temperature.csv")

    print("Обробка завершена. Результати збережено у CSV-файли.")