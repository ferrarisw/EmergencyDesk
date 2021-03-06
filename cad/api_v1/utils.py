import datetime
import googlemaps

from cad.api_v1 import api
from cad.decorators import json
from cad.static import GMAPS_CONF, GMAPS_TOP_RESPONSES, GMAPS_ELEMENT_RESPONSES


@api.route('/utils/geocode/<string:query>', methods=['GET'])
@json
def geocode(query):
    gm = googlemaps.Client(key=GMAPS_CONF['api_key'])
    data = gm.geocode(query, language=GMAPS_CONF['language'])

    if not data:
        return {'Error': 'No Data Found'}

    data = data[0]

    geocoded_data = {'address_components': {}}

    for item in data['address_components']:
        for category in item['types']:
            data[category] = {}
            data[category] = item['long_name']
    geocoded_data['address_components']['country'] = data.get("country", None)
    geocoded_data['address_components']['administrative_area_level_1'] = data.get("administrative_area_level_1", None)
    geocoded_data['address_components']['administrative_area_level_2'] = data.get("administrative_area_level_2", None)
    geocoded_data['address_components']['administrative_area_level_3'] = data.get("administrative_area_level_3", None)
    geocoded_data['address_components']['administrative_area_level_4'] = data.get("administrative_area_level_4", None)
    geocoded_data['address_components']['administrative_area_level_5'] = data.get("administrative_area_level_5", None)
    geocoded_data['address_components']['locality'] = data.get("locality", None)
    geocoded_data['address_components']['sublocality'] = data.get("sublocality", None)
    geocoded_data['address_components']['subpremise'] = data.get("subpremise", None)
    geocoded_data['address_components']['postal_town'] = data.get("postal_town", None)
    geocoded_data['address_components']['postal_code'] = data.get("postal_code", None)
    geocoded_data['address_components']['postal_code_suffix'] = data.get("postal_code_suffix", None)
    geocoded_data['address_components']['neighborhood'] = data.get("neighborhood", None)
    geocoded_data['address_components']['route'] = data.get("route", None)
    geocoded_data['address_components']['street_number'] = data.get('street_number', None)
    geocoded_data['address_components']['housenumber'] = data.get("housenumber", None)

    geocoded_data['formatted_address'] = data['formatted_address']
    geocoded_data['place_id'] = data['place_id']
    geocoded_data['last_update'] = datetime.datetime.now()

    # GEOMETRY

    if GMAPS_CONF['extended_data']:
        geocoded_data['geometry'] = {}
        geocoded_data['geometry']['viewport'] = {}
        geocoded_data['geometry']['location'] = {}
        geocoded_data['geometry']['viewport']['northeast'] = {}
        geocoded_data['geometry']['viewport']['southwest'] = {}

        geocoded_data['types'] = data['types']

        geocoded_data['geometry']['location_type'] = data['geometry']['location_type']
        geocoded_data['geometry']['location']['lat'] = data['geometry']['location']['lat']
        geocoded_data['geometry']['location']['lng'] = data['geometry']['location']['lng']
        geocoded_data['geometry']['viewport']['northeast']['lat'] = data['geometry']['viewport']['northeast']['lat']
        geocoded_data['geometry']['viewport']['northeast']['lng'] = data['geometry']['viewport']['southwest']['lng']
        geocoded_data['geometry']['viewport']['southwest']['lat'] = data['geometry']['viewport']['northeast']['lat']
        geocoded_data['geometry']['viewport']['southwest']['lng'] = data['geometry']['viewport']['southwest']['lng']
    else:
        geocoded_data['address_components']['lat'] = data.get("geometry", {}).get("location", {}).get("lat", None)
        geocoded_data['address_components']['lng'] = data.get("geometry", {}).get("viewport", {}).get("lng", None)
        geocoded_data['address_components']['location_type'] = data.get("geometry", {}).get("location_type", None)

    return geocoded_data


@api.route('/utils/distance/<string:origin>/<string:destination>', methods=['GET'])
@json
def distance(origin, destination):
    gm = googlemaps.Client(key=GMAPS_CONF['api_key'])
    distance_matrix = gm.distance_matrix(origin,
                                         destination,
                                         mode=GMAPS_CONF['mode'],
                                         units=GMAPS_CONF['units'],
                                         departure_time=GMAPS_CONF['departure_time'],
                                         traffic_model=GMAPS_CONF['traffic_model'],
                                         language=GMAPS_CONF['language'])

    top_level_response = distance_matrix['status']
    element_level_response = distance_matrix['rows'][0]['elements'][0]['status']

    if top_level_response == 'OK' and element_level_response == 'OK':

        duration = {}
        duration_in_traffic = {}
        distance = {}
        airline_distance = {}

        duration['meters'] = distance_matrix['rows'][0]['elements'][0]['duration']['value']
        duration['minutes'] = int(distance_matrix['rows'][0]['elements'][0]['duration']['value'] / 60)
        duration['text'] = distance_matrix['rows'][0]['elements'][0]['duration']['text']

        duration_in_traffic['meters'] = distance_matrix['rows'][0]['elements'][0]['duration_in_traffic']['value']
        duration_in_traffic['minutes'] = int(
            distance_matrix['rows'][0]['elements'][0]['duration_in_traffic']['value'] / 60)
        duration_in_traffic['text'] = distance_matrix['rows'][0]['elements'][0]['duration_in_traffic']['text']

        distance['meters'] = distance_matrix['rows'][0]['elements'][0]['distance']['value']
        distance['km'] = distance_matrix['rows'][0]['elements'][0]['distance']['value'] / 1000
        distance['text'] = distance_matrix['rows'][0]['elements'][0]['distance']['text']

        if GMAPS_CONF['airline_distance']:
            import geopy.distance

            from cad.utils import get_lat_lng, get_compass_bearing
            coords_1 = get_lat_lng(origin)
            coords_2 = get_lat_lng(destination)
            compass_bearing = get_compass_bearing(coords_1, coords_2)

            airline_distance['meters'] = round(geopy.distance.vincenty(coords_1, coords_2).meters, 2)
            airline_distance['km'] = round(geopy.distance.vincenty(coords_1, coords_2).km, 2)
            airline_distance['miles'] = round(geopy.distance.vincenty(coords_1, coords_2).miles, 2)
            airline_distance['compass_bearing'] = round(compass_bearing, 2)

        return {
            'origin_address': distance_matrix['origin_addresses'][0],
            'destination_address': distance_matrix['destination_addresses'][0],
            'duration': duration,
            'duration_in_traffic': duration_in_traffic,
            'distance': distance,
            'airline distance': airline_distance,
            'data_age': datetime.datetime.now()
        }
    else:
        if top_level_response is not 'OK':
            return {top_level_response: GMAPS_TOP_RESPONSES[top_level_response]}
        elif element_level_response is not 'OK':
            return {top_level_response: GMAPS_ELEMENT_RESPONSES[element_level_response]}
