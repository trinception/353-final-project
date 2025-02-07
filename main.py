import numpy as np
import pandas as pd
import sys

from amenities_nearby import closest_amenities
from generate_map import form_map, generate_img_path, insert_OSM
from generate_info import generate_point_info
from select_amenity import select_amenites

def main(arg1, arg2,arg3):
    # get picture list from list
    img_path = generate_img_path(arg1)
    map = form_map(img_path)
    osm_path = pd.read_json(arg2, lines= True )
    osm_path = osm_path[osm_path['tags']!={}]

    osm_path = select_amenites(osm_path,img_path,arg3)

    amenity_list = pd.DataFrame()
    for i in range(len(img_path)):
        amenity_list = pd.concat([amenity_list, closest_amenities(img_path.iloc[i],osm_path)])
    amenity_list = amenity_list.drop_duplicates(['lat','lon'])
    amenity_list = amenity_list.dropna(subset = ['name'])
    amenity_list = amenity_list.reset_index().drop(columns=['index'])
    info_list = generate_point_info(amenity_list)
    insert_OSM(map,amenity_list,info_list).save('map.html')


if __name__=='__main__':
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
   
    main(arg1, arg2,arg3)
