# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


##################################################
# import modules

import os
import pandas as pd
import requests
# from tqdm import tqdm
import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from pyproj import CRS
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.lines as mlines
import matplotlib.ticker as ticker
import seaborn as sns
from collections import Counter
import re

from matplotlib import font_manager, rc
plt.rc('font', family='NanumGothic')
print(plt.rcParams['font.family'])

# Set the max_columns option to None
pd.set_option('display.max_columns', None)

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'


##################################################
# set working directory

#define folder where data are stored
base_path = "/Users/USER/PycharmProjects/genderSortingAcrossElementarySchoolInKorea"

cwd = os.getcwd()
# print(cwd)

path_engineered_data = os.path.join(cwd, r'engineered_data')

if not os.path.exists(path_engineered_data):
   os.makedirs(path_engineered_data)


##################################################
# plot school districts (Middle - Elementary, High - Elementary, High - Middle)

# Open school districts shp files
# read elementary school district shp file
file_name = "data/elementarySchooldistrict/초등학교통학구역.shp"
file_path = os.path.join(base_path, file_name)
shapefile = gpd.read_file(file_path)

columns_to_drop = ['CRE_DT', 'UPD_DT', 'BASE_DT']
shapefile_subset = shapefile.drop(columns_to_drop, axis=1)
subsetElementary = shapefile_subset[shapefile_subset['EDU_UP_NM'] == "서울특별시교육청"]

# read middle school district shp file
file_name = "data/middleSchoolDistrict/중학교학교군.shp"
file_path = os.path.join(base_path, file_name)
shapefileMiddle = gpd.read_file(file_path)

columns_to_drop = ['CRE_DT', 'UPD_DT', 'BASE_DT']
shapefileMiddle_subset = shapefileMiddle.drop(columns_to_drop, axis=1)
subsetMiddle = shapefileMiddle_subset[shapefileMiddle_subset['EDU_UP_NM'] == "서울특별시교육청"]

# read high school district shp file
file_name = "data/highSchoolDistrict/고등학교학교군.shp"
file_path = os.path.join(base_path, file_name)
shapefileHigh = gpd.read_file(file_path)

columns_to_drop = ['CRE_DT', 'UPD_DT', 'BASE_DT']
shapefileHigh_subset = shapefileHigh.drop(columns_to_drop, axis=1)
subsetHigh = shapefileHigh_subset[shapefileHigh_subset['EDU_UP_NM'] == "서울특별시교육청"]


# Create a new plot
# base
fig, ax = plt.subplots(figsize=(10, 10))

# 지도: 중학교 학교군 + 초등학교 학교군
# Plot shapefile A
subsetMiddle.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=2, label='중학교 학군')
line_A = mlines.Line2D([], [], color='black', linewidth=2, label='Shapefile A (Bold Line)')

# Plot shapefile B
subsetElementary.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1, linestyle='dotted', label='초등학교 학군')
line_B = mlines.Line2D([], [], color='black', linewidth=1, linestyle='dotted', label='Shapefile B (Dotted Line)')

# Set the aspect ratio to 'equal' for a proper spatial representation
ax.set_aspect('equal')

# Format tick labels
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.4f}'))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.4f}'))

# Remove tick labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Create custom legend handles
handles = [line_A, line_B]
labels = ['중학교 학군', '초등학교 학군']

# Set labels for custom legend handles
for handle, label in zip(handles, labels):
    handle.set_label(label)

# Add legend
plt.legend(handles=handles)

# Add any additional customization as needed (title, legend, etc.)
ax.set_title('Middle and Elementary School Districts of Seoul')

# Specify the file path for saving the figure
file_path = os.path.join(base_path, 'schoolDistricts(MiddleElementarySchool.png')

# Save the figure
plt.savefig(file_path)

# Specify the file path for saving the figure for current project folder
file_path = os.path.join(cwd, 'schoolDistricts(MiddleElementarySchool.png')

# Save the figure
plt.savefig(file_path)

# Display the plot
plt.show()

# 지도: 고등학교 학교군 + 초등학교 학교군
# base
fig, ax = plt.subplots(figsize=(10, 10))

# Plot shapefile A
subsetHigh.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=2, label='고등학교 학군')
line_A = mlines.Line2D([], [], color='black', linewidth=2, label='Shapefile A (Bold Line)')

# Plot shapefile B
subsetElementary.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1, linestyle='dotted', label='초등학교 학군')
line_B = mlines.Line2D([], [], color='black', linewidth=1, linestyle='dotted', label='Shapefile B (Dotted Line)')

# Set the aspect ratio to 'equal' for a proper spatial representation
ax.set_aspect('equal')

# Format tick labels
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.4f}'))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.4f}'))

# Remove tick labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Create custom legend handles
handles = [line_A, line_B]
labels = ['고등학교 학군', '초등학교 학군']

# Set labels for custom legend handles
for handle, label in zip(handles, labels):
    handle.set_label(label)

# Add legend
plt.legend(handles=handles)

# Add any additional customization as needed (title, legend, etc.)
ax.set_title('High and Elementary School Districts of Seoul')

# Specify the file path for saving the figure
file_path = os.path.join(base_path, 'schoolDistricts(HighElementarySchool.png')

# Save the figure
plt.savefig(file_path)

# Specify the file path for saving the figure for current project folder
file_path = os.path.join(cwd, 'schoolDistricts(HighElementarySchool.png')

# Save the figure
plt.savefig(file_path)

# Display the plot
plt.show()

# 지도: 고등학교 학교군 + 중학교 학교군
# base
fig, ax = plt.subplots(figsize=(10, 10))

# Plot shapefile A
subsetHigh.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=2, label='고등학교 학군')
line_A = mlines.Line2D([], [], color='black', linewidth=2, label='Shapefile A (Bold Line)')

# Plot shapefile B
subsetMiddle.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1, linestyle='dotted', label='중학교 학군')
line_B = mlines.Line2D([], [], color='black', linewidth=1, linestyle='dotted', label='Shapefile B (Dotted Line)')

# Set the aspect ratio to 'equal' for a proper spatial representation
ax.set_aspect('equal')

# Format tick labels
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.4f}'))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.4f}'))

# Remove tick labels
ax.set_xticklabels([])
ax.set_yticklabels([])

# Create custom legend handles
handles = [line_A, line_B]
labels = ['고등학교 학군', '중학교 학군']

# Set labels for custom legend handles
for handle, label in zip(handles, labels):
    handle.set_label(label)

# Add legend
plt.legend(handles=handles)

# Add any additional customization as needed (title, legend, etc.)
ax.set_title('High and Middle School Districts of Seoul')

# Specify the file path for saving the figure
file_path = os.path.join(base_path, 'schoolDistricts(HighMiddleSchool.png')

# Save the figure
plt.savefig(file_path)

# Specify the file path for saving the figure for current project folder
file_path = os.path.join(cwd, 'schoolDistricts(HighMiddleSchool.png')

# Save the figure
plt.savefig(file_path)

# Display the plot
plt.show()

