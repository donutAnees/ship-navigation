import math
import os
import xarray as xr
import numpy as np
import pandas as pd
import random
from tqdm import tqdm
from calculatefuel import gridconsumption
from calculaterisk import *
from shipSpeed import *
from grid import *

'''
using grid number and the distance, from the calculate_orientation_distance function's output, and using this grid, dist look at the dataset and for the grid's location, gather the data
how we go about this:
mid points are the grid-identifiers
grid numbers are like 1,2,3,4.... and convert this to corr lat long which are mid points and use these mid-points to extract wave height, wind speed etc from the dataset and with the data, run the calculateRisk, calculateFuel, shipSpeed to get the risk and fuel for the grid in risk_fuel_matrix [ r f]
'''
'''
    what calculate_orientation_and_distance returns:
    A grid where for each grid cell that the ship passes through, we record the orientation of the ship within that cell and the distance it travels between two points, relative to the north direction, as (orientation, distance). If the ship does not travel through a grid cell, it is represented as -1.
'''
step_size=0.8
base_path1=r'C:\Users\deeps\Downloads\academia\sih 2024\codes\dataset_converted\waves_2023-001'

start_lat1=90
start_lon1=90

def extract_data_from_converted_dataset(base_path, lat, lon):
    matched_data = []
    # read from nc and based on the lat lon, get data
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                matched_rows = df[(df['lat'] == lat) & (df['lon'] == lon)]
                if not matched_rows.empty:
                    matched_data.extend(matched_rows.to_dict(orient='records'))
    # convert matched_data to dataframe for better readibility
    matched_df = pd.DataFrame(matched_data)
    return matched_df

base_path_1=r"C:\Users\deeps\Downloads\academia\sih 2024\codes\waves_2023-001"
base_path_2=r"C:\Users\deeps\Downloads\academia\sih 2024\codes\Hackathon-20240905T154632Z-002"
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


def calculate_speed(ship_speed,wave_height, displacement,k1, k2, k3, k4, wind_speed, angle):
    V0=ship_speed
    h=wave_height
    D=displacement
    Vw=wind_speed
    q=angle

    wave_impact = (k1 - k2) * h
    wind_impact = k3 * 10**-3 * Vw * math.cos(math.radians(q))
    environmental_impact = wave_impact + wind_impact
    displacement_impact = 1 - (k4 * 10**-7 * D * V0)
    speed = V0 - (environmental_impact * displacement_impact)
    return speed

def lat_lon_extraction_nonono(x0,y0,x1,y1, start_lat1, start_lon1,step_size):
    lon1 = x0 * step_size + start_lon1
    lat1 = start_lat1 - y0 * step_size
    lon2 = y1 * step_size + start_lon1
    lat2 = start_lat1 - x1 * step_size
    return lat1, lon1, lat2, lon2

def lat_lon_extraction(grid_index, start_lat1, start_lon1,step_size):
    lon1 = grid_index * step_size + start_lon1
    lat1 = grid_index * step_size + start_lat1
    return lat1, lon1

grid=[(110.1282656156892, 0.0), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894085), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894085), (110.1282656156892, 0.8837135479078406), -1, -1, -1, -1, -1, (110.1282656156892, 0.17674270958156796), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894085), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894087), (110.1282656156892, 0.7069708383262727), -1, -1, -1, -1, -1, (110.1282656156892, 0.3534854191631359), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894085), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894087), (110.1282656156892, 0.5302281287447044), -1, -1, -1, -1, -1, (110.1282656156892, 0.5302281287447043), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894087), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894087), (110.1282656156892, 0.35348541916313675), -1, -1, -1, -1, -1, (110.1282656156892, 0.7069708383262718), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894085), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894085), (110.1282656156892, 0.17674270958156946), -1, -1, -1, -1, -1, (110.1282656156892, 0.8837135479078393), -1, -1, -1, -1, -1, (110.1282656156892, 1.0604562574894085), -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
# count the number of entries, -1
count=0
for i in grid:
    if i != -1:
        count+=1
print(count)
print(len(grid))

def risk_fuel_matrix_maker(grid, step_size):
    cc=0
    fr_matrix = []

    for i, cell in enumerate(grid):
        if cell != -1:  # ensuring tht da ship passed thru the cell
            orientation, distance = cell
            cc+=1

            print(f"count of non- -1 grid values: {cc}")
            print(f"orientation, distance of {i+1} : {orientation}, {distance}")
            
            latitude, longitude = lat_lon_extraction(i+1, start_lat1=start_lat1,start_lon1=start_lon1,step_size=step_size)
            print(f"lat, lon: {latitude}, {longitude}")

            #data=extract_data_from_dataset(base_path1,latitude,longitude)
            '''
            if not data.empty():
                print(data.iloc[0])
            else:
                print(f"No data found for lat={latitude}, lon={longitude}. Skipping...")
                fr_matrix.append([-1, -1])
                continue
            '''

            # decode data
            '''
                    numbering goes from bottom to top
                    use desmos to get plot the points
                    omni calculator for equation
                    map: This could refer to a geographical map or a set of coordinates for plotting various data points like wind, waves, or currents.
                    dpt: Likely stands for depth. This might represent the depth of the ocean at specific points in the dataset.
                    uwnd: Refers to the u-component of wind, which is the eastward (or westward) component of the wind vector. It measures how fast the wind is blowing along the east-west axis.
                    vwnd: Refers to the v-component of wind, which is the northward (or southward) component of the wind vector. It measures how fast the wind is blowing along the north-south axis.
                    hs: Most likely refers to significant wave height. This is the average height of the highest third of the waves over a certain period.
                    lm: This could represent mean wavelength, indicating the average wavelength of ocean waves.
                    t02: Could represent the zero-crossing period (also known as wave period). It measures the time between two consecutive zero-crossings of the water sufrace.
                    t01: Likely similar to t02, but possibly a different method of measuring the wave period, such as a more precise or alternate calculation.
                    fp: Likely refers to the peak wave frequency. This is the frequency at which the energy in the waves is highest.
                    dir: Likely refers to wave direction, indicating the direction from which the waves are coming.
                    spr: Could represent wave spreading. This measures how much the wave energy is spread out across different directions.
                    dp: Likely represents the dominant wave period. This is the period associated with the most energetic waves in the dataset.
                    phs00: Likely refers to phase information at level 00, representing the phase of the waves in a given grid point.
                    phs01: Likely refers to phase information at level 01. It could represent the phase of different wave components.
                    ptp00: Could be potential temperature at level 00, representing the temperature of a parcel of water or air if moved adiabatically to a reference pressure.
                    ptp01: Same as ptp00, but at level 01.
                    pdi00: Likely potential density index at level 00, representing the density of water at a specific temperature and pressure.
                    pdi01: Same as pdi00, but at level 01.
                '''
            ship_speed=10.0 # 10 nauts per hour, speed of the ship in still water, can be the top speed of the ship but usually, the ship uses its economical speed (for on fuel consumption and economical factors)
            wave_height= 30.0
            displacement=distance # corr grid identifier's distance from calculate_orientation_and_distance function's output
            k1, k2, k3, k4=1.08, 0.126, 2.77, 2.33
            wind_speed=20.0
            angle=orientation #q or ship's heading, orientation from calculate_orientation_and_distance function's output
            speed_of_the_ship=calculate_speed(ship_speed,wave_height, displacement,k1, k2, k3, k4, wind_speed, angle)
            print(f"speed of the ship is {speed_of_the_ship}")

            #🔽the values of the parameters below can be found in the paper⬇️
            len_of_the_voyage_dist=32000
            fuel_consumption_rate_of_the_ship=50
            power_of_the_main_engine=5000
            cost_of_fuel_per_ton=35
            fuel_consumption=gridconsumption(speed_of_the_ship, len_of_the_voyage_dist, fuel_consumption_rate_of_the_ship,power_of_the_main_engine, cost_of_fuel_per_ton)
            print(f"fuel consumption is {fuel_consumption}")

            # random integer between a range

            ship_heading=random.randint(20,30)
            wave_direction=random.randint(20,30)
            wind_direction=random.randint(20,30)
            wind_angle, wave_angle=find_relative_angles(ship_heading,wave_direction,wind_direction)
            # identify risk based on the wind_angle, wave_angle
            total_risk, risky=navigation_risk(wind_angle, wave_angle)
            print(f"total risk is {total_risk}")

            #fr matrix based on risk_level and fuel_consumption
            fr_matrix.append([fuel_consumption,total_risk])
        else:
            fr_matrix.append([-1,-1])

    return fr_matrix

fr_matrix = risk_fuel_matrix_maker(grid, step_size)
for idx,fr in enumerate(fr_matrix):
    print (idx,fr)
print(fr_matrix)
