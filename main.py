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
# print(plt.rcParams['font.family'])

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
# print(subsetElementary.shape)

# read middle school district shp file
file_name = "data/middleSchoolDistrict/중학교학교군.shp"
file_path = os.path.join(base_path, file_name)
shapefileMiddle = gpd.read_file(file_path)

columns_to_drop = ['CRE_DT', 'UPD_DT', 'BASE_DT']
shapefileMiddle_subset = shapefileMiddle.drop(columns_to_drop, axis=1)
subsetMiddle = shapefileMiddle_subset[shapefileMiddle_subset['EDU_UP_NM'] == "서울특별시교육청"]
# print(len(subsetMiddle))

# read high school district shp file
file_name = "data/highSchoolDistrict/고등학교학교군.shp"
file_path = os.path.join(base_path, file_name)
shapefileHigh = gpd.read_file(file_path)

columns_to_drop = ['CRE_DT', 'UPD_DT', 'BASE_DT']
shapefileHigh_subset = shapefileHigh.drop(columns_to_drop, axis=1)
subsetHigh = shapefileHigh_subset[shapefileHigh_subset['EDU_UP_NM'] == "서울특별시교육청"]

# columns = subsetMiddle.columns
# for col in columns:
#     print(col)
# print(subsetMiddle['HAKGUDO_NM'])

'''
### test: find valid elementary school polygons in each polygon of Middle school distrcits
# use "강남서초4학교군" for test
subsetMiddleGangnam4 = subsetMiddle[subsetMiddle['HAKGUDO_NM'] == "중부4학교군"]

# Calculate the area of each polygon in subsetElementary
subsetElementary['area'] = subsetElementary.geometry.apply(lambda x: x.area)
# print(subsetElementary['area'])
intersection_result = gpd.overlay(subsetMiddleGangnam4, subsetElementary, how='intersection')

# Calculate the area of each intersected polygon
intersection_result['areaIntersected'] = intersection_result.geometry.area
# print(intersection_result['areaIntersected'])

# print(intersection_result['HAKGUDO_NM_2'])
# print(subsetElementary['HAKGUDO_NM'])
print(intersection_result.head())
print(subsetElementary.head())

# Merge the DataFrames based on the specified key and add the 'area' column
merged_result = pd.merge(intersection_result, subsetElementary[['HAKGUDO_NM']],
                         left_on='HAKGUDO_NM_2', right_on='HAKGUDO_NM', how='left')

merged_result['intersectedAreaShare'] = merged_result['areaIntersected'] / merged_result['area'] * 100

# Print the merged result
print(merged_result)

# Plotting subsetMiddleGangnam4
ax = subsetMiddleGangnam4.plot(color='blue', alpha=0.5)

# Plotting subsetElementary
subsetElementary.plot(ax=ax, color='red', alpha=0.5)

plt.show()
'''

##################################################
# add area info in each shp file
subsetElementary['geometry'] = subsetElementary.geometry.buffer(0)
subsetMiddle['geometry'] = subsetMiddle.geometry.buffer(0)
subsetHigh['geometry'] = subsetHigh.geometry.buffer(0)

subsetElementary['ElementaryDistrictArea'] = subsetElementary.geometry.apply(lambda x: x.area)
subsetMiddle['MiddleDistrictArea'] = subsetMiddle.geometry.apply(lambda x: x.area)
# subsetHigh['HighDistrictArea'] = subsetHigh.geometry.apply(lambda x: x.area)


##################################################
# count number of Elementary school districts in Middle school districts
middleHakgudo = subsetMiddle['HAKGUDO_NM'].unique()

dictMiddleElementaryHakgudoCounts = dict()
for Hakgudo in middleHakgudo:
    # get subset of middle school hakgudo one by one
    tempDF = subsetMiddle[subsetMiddle['HAKGUDO_NM'] == Hakgudo]
    # intersect tempDF with subsetElementary to find polygons over tempDF
    tempIntersection = gpd.overlay(tempDF, subsetElementary, how='intersection')
    # get intersected polygons' area
    tempIntersection['areaIntersected'] = tempIntersection.geometry.area
    # get intersected polygons' area share
    merged_result = pd.merge(tempIntersection, subsetElementary[['HAKGUDO_NM']],
                             left_on='HAKGUDO_NM_2', right_on='HAKGUDO_NM', how='left')
    merged_result['intersectedAreaShare'] = merged_result['areaIntersected'] / merged_result['ElementaryDistrictArea'] * 100
    # # Filter rows where intersectedAreaShare > 95
    merged_result_filtered = merged_result[merged_result['intersectedAreaShare'] > 5]
    dictMiddleElementaryHakgudoCounts[Hakgudo] = len(merged_result_filtered)

countMiddleElementaryDF = pd.DataFrame(list(dictMiddleElementaryHakgudoCounts.items()), columns=['HAKGUDO_NM', 'ElementarySchoolDistrictsCount'])
# print(countMiddleElementaryDF)

# Calculate the sum of values
# Display the sum: this could be different from the total number of elementary school districts because of shared school districts
sum_values = countMiddleElementaryDF['ElementarySchoolDistrictsCount'].sum()
print("Sum of values:", sum_values)
print(len(subsetElementary))

subsetMiddle = pd.merge(subsetMiddle, countMiddleElementaryDF,
                             left_on='HAKGUDO_NM', right_on='HAKGUDO_NM', how='left')
# print(subsetMiddle.head())


##################################################
# count number of Elementary school districts in High school districts
highHakgudo = subsetHigh['HAKGUDO_NM'].unique()

dictHighElementaryHakgudoCounts = dict()
for Hakgudo in highHakgudo:
    # get subset of middle school hakgudo one by one
    tempDF = subsetHigh[subsetHigh['HAKGUDO_NM'] == Hakgudo]
    # intersect tempDF with subsetElementary to find polygons over tempDF
    tempIntersection = gpd.overlay(tempDF, subsetElementary, how='intersection')
    # get intersected polygons' area
    tempIntersection['areaIntersected'] = tempIntersection.geometry.area
    # get intersected polygons' area share
    merged_result = pd.merge(tempIntersection, subsetElementary[['HAKGUDO_NM']],
                             left_on='HAKGUDO_NM_2', right_on='HAKGUDO_NM', how='left')
    # print(merged_result.columns)
    merged_result['intersectedAreaShare'] = merged_result['areaIntersected'] / merged_result['ElementaryDistrictArea'] * 100
    # Filter rows where intersectedAreaShare > 95
    merged_result_filtered = merged_result[merged_result['intersectedAreaShare'] > 5]
    dictHighElementaryHakgudoCounts[Hakgudo] = len(merged_result_filtered)

# print(dictMiddleHakgudoCounts)
countHighElementaryDF = pd.DataFrame(list(dictHighElementaryHakgudoCounts.items()), columns=['HAKGUDO_NM', 'ElementarySchoolDistrictsCount'])
# print(countHighElementaryDF)

# Calculate the sum of values
# Display the sum: this could be different from the total number of elementary school districts because of shared school districts
sum_values = countHighElementaryDF['ElementarySchoolDistrictsCount'].sum()
print("Sum of values:", sum_values)
print(len(subsetElementary))

subsetHigh = pd.merge(subsetHigh, countHighElementaryDF,
                             left_on='HAKGUDO_NM', right_on='HAKGUDO_NM', how='left')
# print(subsetHigh.head())

##################################################
# count number of Middle school districts in High school districts
highHakgudo = subsetHigh['HAKGUDO_NM'].unique()

dictHighMiddleHakgudoCounts = dict()
for Hakgudo in highHakgudo:
    # get subset of middle school hakgudo one by one
    tempDF = subsetHigh[subsetHigh['HAKGUDO_NM'] == Hakgudo]
    # intersect tempDF with subsetElementary to find polygons over tempDF
    tempIntersection = gpd.overlay(tempDF, subsetMiddle, how='intersection')
    # get intersected polygons' area
    tempIntersection['areaIntersected'] = tempIntersection.geometry.area
    # get intersected polygons' area share
    merged_result = pd.merge(tempIntersection, subsetMiddle[['HAKGUDO_NM']],
                             left_on='HAKGUDO_NM_2', right_on='HAKGUDO_NM', how='left')
    # print(merged_result.columns)
    merged_result['intersectedAreaShare'] = merged_result['areaIntersected'] / merged_result['MiddleDistrictArea'] * 100
    # Filter rows where intersectedAreaShare > 95
    merged_result_filtered = merged_result[merged_result['intersectedAreaShare'] > 5]
    dictHighMiddleHakgudoCounts[Hakgudo] = len(merged_result_filtered)

# print(dictMiddleHakgudoCounts)
countHighMiddleDF = pd.DataFrame(list(dictHighMiddleHakgudoCounts.items()), columns=['HAKGUDO_NM', 'MiddleSchoolDistrictsCount'])
# print(countHighMiddleDF)

# Calculate the sum of values
# Display the sum: this could be different from the total number of elementary school districts because of shared school districts
sum_values = countHighMiddleDF['MiddleSchoolDistrictsCount'].sum()
print("Sum of values:", sum_values)
print(len(subsetMiddle))

subsetHigh = pd.merge(subsetHigh, countHighMiddleDF,
                             left_on='HAKGUDO_NM', right_on='HAKGUDO_NM', how='left')
# print(subsetMiddle)
# print(subsetHigh)
print(subsetMiddle[['HAKGUDO_NM', 'ElementarySchoolDistrictsCount']])
print(subsetHigh[['HAKGUDO_NM','MiddleSchoolDistrictsCount','ElementarySchoolDistrictsCount']])


#################################################
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
# plt.legend(handles=handles)

# Add any additional customization as needed (title, legend, etc.)
ax.set_title('Middle and Elementary School Districts of Seoul')

# Create a new column in the subsetMiddle dataframe to store the count
subsetMiddle['num_polygons'] = 0

# Iterate over each polygon in subsetMiddle
for index, row in subsetMiddle.iterrows():
    polygon = row['geometry']
    count = 0

    # Check if the polygon contains any polygons from subsetElementary
    for _, elem_row in subsetElementary.iterrows():
        elem_polygon = elem_row['geometry']
        if polygon.contains(elem_polygon):
            count += 1

    # Update the 'num_polygons' column with the count
    subsetMiddle.loc[index, 'num_polygons'] = count

# Print only the 'HAKGUDO_NM' and 'num_polygons' columns
print(subsetMiddle[['HAKGUDO_NM', 'num_polygons']])

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

