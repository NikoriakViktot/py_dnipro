
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

file_path ='C:\\Users\\user\\OneDrive\\Documents\\CURVE\\curve_rozymivka.xlsx'

data = pd.read_excel(file_path)
data['h'] = data['h'] / 100  # Convert cm to meters if necessary

# Your additional data
additional_data = pd.DataFrame({
    'h': [18.86, 18.32, 18.09, 17.94, 17.85, 17.70, 17.41, 16.87],
    'Q': [23800, 19200, 16200, 14200, 13100, 11400, 9400, 7200]
})

# Combine the data from the Excel file and the additional data
combined_data = pd.concat([data, additional_data], ignore_index=True)

# Polynomial features transformation
poly = PolynomialFeatures(degree=4)
X = combined_data['h'].values.reshape(-1, 1)
X_poly = poly.fit_transform(X)
y = combined_data['Q'].values
weights = np.ones_like(y)
weights[y > 10000] = 10
# Fit a linear regression model with the full dataset
model = LinearRegression().fit(X_poly, y, sample_weight=weights)

# Generate predictions for a specific range of water levels
h_range = np.linspace(11.5, 20, 50).reshape(-1, 1)
predictions = model.predict(poly.transform(h_range))

# Create a dataframe for these specific predictions
predictions_df = pd.DataFrame({
    'h': h_range.flatten(),
    'Q': predictions
})

# Save predictions to a CSV file
# predictions_df.to_csv('WaterLevels_11.5_to_22_Predictions.csv', index=False)

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(X, y, color='blue', label='Витрати води за 1952-53 рр.')
plt.scatter(additional_data['h'], additional_data['Q'], color='black', marker='x', s=100, label='Підпірні витрати Дніпровського водосховща')
plt.plot(h_range, predictions, color='red', label='Поліноміальна регресійна модель (4 порядку)')
plt.xlabel('h  (м)')
plt.ylabel(' Q  (m3/c)')
plt.title('Поліноміальна регресійна модель, \n'
          'що ілюструє залежність між рівнем води  та витратами води в  с.Розумівка')


plt.legend()
plt.grid(True)
plt.show()
