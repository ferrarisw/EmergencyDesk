import googlemaps

from cad.api_v1 import api
from cad.decorators import json

GOOGLE_MAPS_API_KEY = 'AIzaSyDV40MOxLr9fo2G1BwxEaA6WBXpZa1Fnjs'

GMAPS_CONF = {
    'API_KEY': 'AIzaSyDV40MOxLr9fo2G1BwxEaA6WBXpZa1Fnjs',
    'mode': 'driving',
    'units': 'metric',
    'departure_time': 'now',
    'traffic_model': 'pessimistic'
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
    gm = googlemaps.Client(key=GMAPS_CONF['API_KEY'])
    geocode_results = gm.geocode(query)
    return geocode_results[0]


@api.route('/utils/formatted_address/<string:query>', methods=['GET'])
@json
def get_formatted_address(query):
    gm = googlemaps.Client(key=GMAPS_CONF['API_KEY'])
    geocode_results = gm.geocode(query)[0]

    return geocode_results['formatted_address']


@api.route('/utils/distance/<string:origin>/<string:destination>', methods=['GET'])
@json
def distance(origin, destination):
    gm = googlemaps.Client(key=GMAPS_CONF['API_KEY'])
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
