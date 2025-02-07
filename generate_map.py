# https://towardsdatascience.com/creating-a-simple-map-with-folium-and-python-4c083abfff94
import numpy as np
import pandas as pd
import folium
import os
import logging

from calc_distance import smooth,distance
from exif_picture import extract_coords


def form_map(locations):
    map = folium.Map(location = [locations.lat.mean(), locations.lon.mean()],zoom_start =30, control_scale=True)
    loc = []
    for index,location_info in locations.iterrows():
        # folium.Marker([location_info['Latitude'],location_info['Longitude']],popup = location_info['name']).add_to(map)
        loc.append((location_info['lat'],location_info['lon']))
    # https://stackoverflow.com/questions/60578408/is-it-possible-to-draw-paths-in-folium
    folium.Marker([locations['lat'].iloc[0],locations['lon'].iloc[0]],popup = 'your start point').add_to(map)
    folium.Marker([locations['lat'].iloc[-1],locations['lon'].iloc[-1]],popup = 'your finish point').add_to(map)
    # print(locations['Latitude'].iloc[0],locations['Longitude'].iloc[0])
    folium.PolyLine(loc,color='blue',weight =5,opacity =0.5).add_to(map)
    return map

def generate_img_path(img_path):
    img_list =os.listdir(img_path)
    img = pd.DataFrame(img_list, columns =['photo_id'],index=None)
    img['photo_id'] = img_path+'/'+img['photo_id']
    extract = np.vectorize(extract_coords)
    (img['lat'],img['lon'],img['datetime']) = extract(img['photo_id'])
    img = img.sort_values(by = ['datetime'])  
    img = img.reset_index().drop(columns=['index'])
    smoothed = smooth(img[['lat','lon']])
    img['lat'] = smoothed['lat']
    img['lon'] = smoothed['lon']
    img = img.sort_values(by = ['datetime'])  
    img = img.reset_index().drop(columns=['index'])

    return img


def insert_OSM(map, osm, info_list):
    if map is None or osm is None or info_list is None:
        logging.error("One or more required parameters is None")
        return map
        
    if len(osm) != len(info_list):
        logging.error(f"Mismatched lengths: osm ({len(osm)}) != info_list ({len(info_list)})")
        return map
        
    try:
        for i in range(len(osm)):
            name = info_list['name'].iloc[i]
            addr = info_list['addr'].iloc[i]
            website = info_list['website'].iloc[i] if 'website' in info_list.columns and pd.notna(info_list['website'].iloc[i]) else ""
            open_hours = info_list['open'].iloc[i] if 'open' in info_list.columns and pd.notna(info_list['open'].iloc[i]) else ""

            info = f"<b>name: </b>{name}<br><b>address: </b>{addr}"
            if open_hours:
                info += f"<br><b>opening hours: </b>{open_hours}"
            if website:
                info += f"<br><b>website: </b><a href={website}>more detail</a>"

            folium.Marker(
                [osm['lat'].iloc[i], osm['lon'].iloc[i]],
                icon=folium.Icon(color='green'),
                popup=info,
                tooltip="Click me!"
            ).add_to(map)

        return map

    except KeyError as e:
        logging.error(f"Missing required column: {e}")
        return map
    except Exception as e:
        logging.error(f"Error inserting OSM data into map: {e}")
        return map