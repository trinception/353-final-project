353 FINAL PROJECT -> Given a set of photos of places to visit, and a theme/amenity of interest, this program generates a map with a path through the places to visit with the theme/amenity of interest highlighted along the route.

**Required libaries:**

pandas: 

    pip3 install pandas

numpy: 

    pip3 install numpy

pykalman: 

    pip3 install pykalman

pyspark:

    pip3 install pyspark

exif: 

    pip3 install exif
or 

    sudo apt-get install exif

folium: 

    pip3 install folium
or 

    conda install -c conda-forge folium
    
**How to run the program:**

To run the program please run the command in form of

    python3 main.py photo_folder amenities-vancouver.json theme_or_amenity_type
Where photo_folder is the folder of photo you want to use, theme is one of the choice of (foods, chill_area (places like bars, social_areas),sightseeing (places like clock, art-center,monastery), all( if average speed that calculated from pictures are smaller than 14, then define the user is wallking or riding bike, which will display things like(food court, sightseeing places or those chill_areas, otherwise we don't know whether user is moving by transportation or randomly choose some picutres, so we will display all the places that meet the requirement))), amenity_type is an amenity type in type_of _amenity.csv.

Example command:

    python3 main.py photo2 amenities-vancouver.json foods

To see the result, please see in the **map.html**, which will shows map of possible place you may look for.


**FUTURE IMPROVEMENTS:**

1. Use a better review dataset than Yelp, like Google Review, which has more reviews and may be more accurate.
2. Add more features to the map, like the distance between the user and the place.
3. Add more features to the map, like the time to the place.
4. Add more features to the map, like the review scores.
5. Modify the paths generated to more accurately adhere to the roads and pathways.