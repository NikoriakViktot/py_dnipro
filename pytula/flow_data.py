import pandas as pd
import os

directory = 'C:/Users/user/PycharmProjects/py_dnipro/pytula/flow_data'

files = [os.path.join(directory, file) for file in os.listdir(directory) if
         file.endswith('.xlsx') and not file.startswith('~$')]

data = []

for file in files:
    year = os.path.basename(file).split('_')[0]

    # Load the Excel file
    xls = pd.ExcelFile(file)

    sheet_name = xls.sheet_names[0]

    df = pd.read_excel(file, sheet_name=sheet_name, skiprows=2)

    # Extract the dates and the data
    dates = df.iloc[:, 0]
    for month in range(1, 13):
        month_data = df.iloc[:, month]
        for i in range(len(dates)):
            if dates[i] == "Декада":
                break
            try:
                day = int(dates[i])
                value = month_data[i]
                if pd.notna(value):
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    data.append([date_str, value])
            except (ValueError, TypeError):
                # Skip rows where the date is not a valid number
                continue

# Convert the list to a DataFrame
df_data = pd.DataFrame(data, columns=["Date", "Value"])

# Save the data to a CSV file in the same directory without header
output_file = os.path.join(directory, 'daily_water_discharge.csv')
df_data.to_csv(output_file, index=False, header=False)

print(f"Data has been saved to {output_file}")
