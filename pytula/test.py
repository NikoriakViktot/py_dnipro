from netCDF4 import Dataset


netcdf_file = rf"C:\Users\user\PycharmProjects\py_dnipro\pytula\data_pytula\era5_data_snow_NetCDF\era5_data_1991_01.nc"

dataset = Dataset(netcdf_file, mode='r')

# Print the list of variables and dimensions
print("Variables in the dataset:")
for var in dataset.variables:
    print(var)

print("\nDimensions in the dataset:")
for dim in dataset.dimensions:
    print(f"{dim}: {len(dataset.dimensions[dim])}")

# Optionally, print detailed information about each variable
for var in dataset.variables:
    print(f"\nDetails of variable '{var}':")
    print(dataset.variables[var])