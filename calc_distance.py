import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import sys
from pykalman import KalmanFilter


def get_data(file):
    parse_result = ET.parse(file)
    points = parse_result.iter('{http://www.topografix.com/GPX/1/0}trkpt')

    gps = pd.DataFrame(columns=['lat', 'lon'])

    for elements in points:
        point = pd.DataFrame([[elements.attrib['lat'], elements.attrib['lon']]], columns=['lat', 'lon'])
        gps = pd.concat([gps, point], ignore_index=True)

    return gps
    
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c * 1000  # Convert to meters

def distance(gps):
    if gps.empty:
        return 0.0

    lat = gps['lat'].astype(float).values
    lon = gps['lon'].astype(float).values

    shifted_lat = np.roll(lat, 1)
    shifted_lon = np.roll(lon, 1)

    # Calculate distances using the Haversine formula
    distances = haversine(shifted_lat[1:], shifted_lon[1:], lat[1:], lon[1:])
    return np.sum(distances)

def smooth(gps):
    kalman_data = pd.DataFrame( gps['lat'].values.astype(float),columns=['lat'])
    kalman_data['lon'] = gps['lon'].values.astype(float)
    
    initial_state = kalman_data.iloc[0]
    observation_covariance = np.diag([2/10000, 2/10000]) ** 2 
    transition_covariance = np.diag([1/10000, 1/10000]) ** 2 
    transition = [[1,0],[0,1]] 


    kf = KalmanFilter(initial_state_mean=initial_state,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition)

    kalman_smoothed, _ = kf.smooth(kalman_data)
    smoothed = pd.DataFrame(kalman_smoothed, columns = ['lat','lon'])
    return smoothed
    

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)
    
    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)
    
    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)
    
    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points),))
    
    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()