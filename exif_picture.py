# https://medium.com/spatial-data-science/how-to-extract-gps-coordinates-from-images-in-python-e66e542af354

import exif

img_path = 'photos/IMG_2787.JPG'


def extract_coords(img_path):
    def decimal_coords(coords, ref):
        decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
        if ref in ['S', 'W']:
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    try:
        with open(img_path, 'rb') as src:
            img = exif.Image(src)

        if not img.has_exif:
            print(f'The image {img_path} has no EXIF information.')
            return None

        if not hasattr(img, 'gps_latitude') or not hasattr(img, 'gps_longitude'):
            print(f'The image {img_path} has no GPS coordinates.')
            return None

        coords = (
            decimal_coords(img.gps_latitude, img.gps_latitude_ref),
            decimal_coords(img.gps_longitude, img.gps_longitude_ref),
            img.datetime
        )
        return coords

    except Exception as e:
        print(f'Error processing {img_path}: {e}')
        return None

