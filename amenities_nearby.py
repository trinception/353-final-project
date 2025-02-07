# nearby_amenities.py
# Given exif data it locates all amenities within a 3 km radius of a given geotagged photo (we can change the distance)
# NOTE** we can refine this to only highlight the "interesting" or "important" sites as well as distance

import pandas as pd
import numpy as np

from math import radians, cos, sin, asin, sqrt

# Distance function and closest_amenities function (below)
# Calculates the distances between a photo and all the amenities
def distance(osm, photo):

    # Transform to radians
    photo_lon, photo_lat, osm_lon, osm_lat = map(radians, [photo.lon, photo.lat, osm.lon, osm.lat])
    longitude_distance = osm_lon - photo_lon
    latitude_distance = osm_lat - photo_lat

    # Calculate area
    area = sin(latitude_distance/2)**2 + cos(photo_lat) * cos(osm_lat) * sin(longitude_distance/2)**2

    # Calculate the central angle
    central_angle = 2 * asin(sqrt(area))
    radius = 6371 #in KM

    # Calculate Distance
    distance = central_angle * radius

    return distance
    #print("checkpoint in distance")

def closest_amenities(photo, osm_data):
    osm_data['distance']=osm_data.apply(distance, photo=photo, axis=1)
    closestAmenities = osm_data[osm_data['distance']<=0.3]

    return closestAmenities

def cal_speed(img_path):
    img_path['speed'] = np.nan
    img_path['datetime'] = pd.to_datetime(img_path.datetime,format = '%Y:%m:%d %H:%M:%S')
    for i in range(len(img_path)-1):
        d = distance(img_path.iloc[i+1],img_path.iloc[i])
        time = (img_path['datetime'].iloc[i+1] - img_path['datetime'].iloc[i]).total_seconds()
        img_path['speed'].iloc[i+1] = d*1000/time # meters/second
    return img_path


    