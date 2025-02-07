import pandas as pd
import math
from amenities_nearby import  cal_speed

def filter_by_amenity(osm_path, amenity_types):
    return osm_path[osm_path['amenity'].isin(amenity_types)]

def select_amenites(osm_path, img_path, arg3):
    food_amenities = {"cafe", "fast_food", "restaurant", "pub", "bar", "ice_cream", "bistro", "food_court", "water_point"}
    chill_amenities = {"cinema", "theatre", "bar", "social_facility", "conference_centre", "nightclub", "gambling", "bistro", "events_venue", "internet_cafe", "social_centre", "smoking_area", "spa", "gym", "biergarten", "shop|clothes"}
    sightseeing_amenities = {"arts_centre", "fountain", "social_facility", "clock", "water_point", "monastery"}

    if arg3 != 'all':
        if arg3 in osm_path['amenity'].values:
            return osm_path[osm_path['amenity'] == arg3]
        elif arg3 == 'foods':
            return filter_by_amenity(osm_path, food_amenities)
        elif arg3 == 'chill_area':
            return filter_by_amenity(osm_path, chill_amenities)
        elif arg3 == 'sightseeing':
            return filter_by_amenity(osm_path, sightseeing_amenities)
        else:
            raise ValueError(f"Invalid choice: {arg3}. Please choose from 'foods', 'chill_area', 'sightseeing', or 'all'.")
    else:
        if len(img_path) < 2:
            return math.inf
        img_path = cal_speed(img_path)
        mean_speed = img_path['speed'].mean()
        if mean_speed <= 5.5:
            all_amenities = food_amenities.union(chill_amenities).union(sightseeing_amenities)
            return filter_by_amenity(osm_path, all_amenities)
    return osm_path