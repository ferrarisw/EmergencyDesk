import googlemaps

from cad.api_v1 import api
from cad.decorators import json

GOOGLE_MAPS_api_key = 'AIzaSyDV40MOxLr9fo2G1BwxEaA6WBXpZa1Fnjs'

GMAPS_CONF = {
    'api_key': 'AIzaSyDV40MOxLr9fo2G1BwxEaA6WBXpZa1Fnjs',
    'departure_time': 'now',
    'language': 'IT',
    'mode': 'driving',
    'traffic_model': 'pessimistic',
    'units': 'metric'
}

GMAPS_TOP_RESPONSES = {
    'OK': 'indicates the response contains a valid result',
    'INVALID_REQUEST': 'The provided request was invalid.',
    'MAX_ELEMENTS_EXCEEDED': 'The product of origins and destinations exceeds the per-query limit.',
    'OVER_QUERY_LIMIT': 'The service has received too many '
                        'requests from your application within the allowed time period.',
    'REQUEST_DENIED': 'The service denied use of the Distance Matrix service by your application.',
    'UNKNOWN_ERROR': 'The Distance Matrix request could not be processed '
                     'due to a server error. The request may succeed if you try again.'
}

GMAPS_ELEMENT_RESPONSES = {
    'OK': 'The response contains a valid result.',
    'NOT_FOUND': 'The origin and/or destination of this pairing could not be geocoded.',
    'ZERO_RESULTS': 'No route could be found between the origin and destination.',
    'MAX_ROUTE_LENGTH_EXCEEDED': 'The requested route is too long and cannot be processed.'
}


@api.route('/utils/geocode/<string:query>', methods=['GET'])
@json
def geocode(query):
    gm = googlemaps.Client(key=GMAPS_CONF['api_key'])
    data = gm.geocode(query, language=GMAPS_CONF['language'])[0]

    geocoded_data = {}

    for item in data['address_components']:
        for category in item['types']:
            data[category] = {}
            data[category] = item['long_name']
    geocoded_data['country'] = data.get("country", None)
    geocoded_data['administrative_area_level_3'] = data.get("administrative_area_level_3", None)
    geocoded_data['administrative_area_level_2'] = data.get("administrative_area_level_2", None)
    geocoded_data['administrative_area_level_1'] = data.get("administrative_area_level_1", None)
    geocoded_data['locality'] = data.get("locality", None)
    geocoded_data['sublocality'] = data.get("sublocality", None)
    geocoded_data['subpremise'] = data.get("subpremise", None)
    geocoded_data['postal_town'] = data.get("postal_town", None)
    geocoded_data['postal_code'] = data.get("postal_code", None)
    geocoded_data['postal_code_suffix'] = data.get("postal_code_suffix", None)
    geocoded_data['neighborhood'] = data.get("neighborhood", None)
    geocoded_data['route'] = data.get("route", None)
    geocoded_data['street_number'] = data.get('street_number', None)
    geocoded_data['housenumber'] = data.get("housenumber", None)
    geocoded_data['latitude'] = data.get("geometry", {}).get("location", {}).get("lat", None)
    geocoded_data['longitude'] = data.get("geometry", {}).get("location", {}).get("lng", None)
    geocoded_data['location_type'] = data.get("geometry", {}).get("location_type", None)
    geocoded_data['formatted_address'] = data['formatted_address']

    return geocoded_data


@api.route('/utils/formatted_address/<string:query>', methods=['GET'])
@json
def get_formatted_address(query):
    gm = googlemaps.Client(key=GMAPS_CONF['api_key'])
    geocode_results = gm.geocode(query)[0]

    return {
        'formatted_address': geocode_results['formatted_address'],
    }


@api.route('/utils/distance/<string:origin>/<string:destination>', methods=['GET'])
@json
def distance(origin, destination):
    gm = googlemaps.Client(key=GMAPS_CONF['api_key'])
    distance_matrix = gm.distance_matrix(origin,
                                         destination,
                                         mode=GMAPS_CONF['mode'],
                                         units=GMAPS_CONF['units'],
                                         departure_time=GMAPS_CONF['departure_time'],
                                         traffic_model=GMAPS_CONF['traffic_model'])

    top_level_response = distance_matrix['status']
    element_level_response = distance_matrix['rows'][0]['elements'][0]['status']

    if top_level_response == 'OK' and element_level_response == 'OK':
        duration = distance_matrix['rows'][0]['elements'][0]['duration']['value']
        duration_in_traffic = distance_matrix['rows'][0]['elements'][0]['duration_in_traffic']['value']
        distance = distance_matrix['rows'][0]['elements'][0]['distance']['value']

        return {
            'duration': duration,
            'duration_in_traffic': duration_in_traffic,
            'distance': distance}
    else:
        if top_level_response is not 'OK':
            return {top_level_response: GMAPS_TOP_RESPONSES[top_level_response]}
        elif element_level_response is not 'OK':
            return {top_level_response: GMAPS_ELEMENT_RESPONSES[element_level_response]}
