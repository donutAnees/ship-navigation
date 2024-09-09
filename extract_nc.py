import os
import numpy as np
import xarray as xr
import pandas as pd

base_path_1="./dataset/wave.nc"
base_path_2="./dataset/current.nc"

def extract_data_from_nc_files(base_path, lat, lon):
    matched_data = []
    # read from nc and based on the lat lon, get data
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".nc"):
                file_path = os.path.join(root, file)
                ds = xr.open_dataset(file_path)
                lats = ds.coords['lat'].values
                lons = ds.coords['lon'].values
                lat_idx = np.argmin(np.abs(lats - lat))
                lon_idx = np.argmin(np.abs(lons - lon))
                data = ds.isel(lat=lat_idx, lon=lon_idx).to_dataframe().reset_index()
                matched_data.append(data)
                #df = ds.to_dataframe()
                #matched_rows = df[(df['lat'] == lat) & (df['lon'] == lon)]
                #if not matched_rows.empty:
                #    matched_data.extend(matched_rows.to_dict(orient='records'))
    # convert matched_data to dataframe for better readibility
    #matched_df = pd.DataFrame(matched_data)
    matched_df = pd.concat(matched_data, ignore_index=True)
    return matched_df


latitude=-45.5
longitude=30.0
base_path1=r'C:\Users\deeps\Downloads\academia\sih 2024\codes\dataset_converted\waves_2023-001'
data=extract_data_from_nc_files(base_path1,latitude,longitude)
print(data)