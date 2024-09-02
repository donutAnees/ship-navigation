import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Path to the highest resolution shapefile (level 6)
shapefile_path = './Data/ne_110m_land.shp'

# Load the dataset using geopandas
land = gpd.read_file(shapefile_path)
land = land.to_crs(epsg=4326)  # WGS84, which uses longitude and latitude
print(land.head())

# Check the CRS of the shapefile
print("Original CRS:", land.crs)

# If the CRS is not EPSG:4326, convert it
if land.crs.to_epsg() != 4326:
    land = land.to_crs(epsg=4326)

# Define your coordinate (longitude, latitude)
def is_land_area(lat, lon):
    coordinate = Point( lon, lat)
    # Check if the point is within any land polygon
    return land.contains(coordinate).any() # problematic line

is_land = is_land_area( 80.519928, 9.283716 )

if is_land:
    print("The coordinate is on land.")
else:
    print("The coordinate is in the sea.")

ax = land.plot(edgecolor='black', alpha=0.5)
# plt.scatter(*coordinate.xy, color='red', label='Test Coordinate')
# plt.legend()
# plt.title('Land Polygons and Test Coordinate')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.show()

