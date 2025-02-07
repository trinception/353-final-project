import pandas as pd
import folium

def generate_point_info(amenities):
    if not isinstance(amenities, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    required_columns = ['name', 'tags']
    if not all(col in amenities.columns for col in required_columns):
        raise ValueError(f"Input DataFrame must contain the following columns: {required_columns}")

    data = pd.DataFrame.from_records(amenities['tags'])
    info_list = pd.DataFrame()
    info_list['name'] = amenities['name']
    info_list['addr'] = data.apply(get_addr, axis=1)
    info_list['website'] = data.apply(get_website, axis=1)
    
    if 'opening_hours' in data:
        info_list['open'] = data['opening_hours']
    
    return info_list

def get_website(tag):
    if not isinstance(tag, dict):
        return ''

    if 'website' in tag and pd.notna(tag['website']):
        return tag['website']
    elif 'brand:wikipedia' in tag and pd.notna(tag['brand:wikipedia']):
        return f"https://en.wikipedia.org/wiki/{tag['brand:wikipedia']}"
    elif 'brand:wikidata' in tag and pd.notna(tag['brand:wikidata']):
        return f"https://www.wikidata.org/wiki/{tag['brand:wikidata']}"
    return ''

def get_addr(tag):
    if not isinstance(tag, dict):
        return ''

    addr_parts = []
    if 'addr:housenumber' in tag and pd.notna(tag['addr:housenumber']):
        addr_parts.append(str(tag['addr:housenumber']))
    if 'addr:street' in tag and pd.notna(tag['addr:street']):
        addr_parts.append(str(tag['addr:street']))
    if 'addr:city' in tag and pd.notna(tag['addr:city']):
        addr_parts.append(str(tag['addr:city']))
    
    return ', '.join(addr_parts)
