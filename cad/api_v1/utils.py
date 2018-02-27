import googlemaps

from cad.api_v1 import api
from cad.decorators import json

API_KEY = 'AIzaSyDV40MOxLr9fo2G1BwxEaA6WBXpZa1Fnjs'


@api.route('/utils/geocode/<string:query>', methods=['GET'])
@json
def geocode(query):
    gm = googlemaps.Client(key=API_KEY)
    geocode_results = gm.geocode(query)
    return geocode_results[0]


@api.route('/utils/formatted_address/<string:query>', methods=['GET'])
@json
def get_formatted_address(query):
    gm = googlemaps.Client(key=API_KEY)
    geocode_results = gm.geocode(query)[0]

    return geocode_results['formatted_address']


@api.route('/utils/distance/<string:origin>/<string:destination>', methods=['GET'])
@json
def distance(origin, destination):
    gm = googlemaps.Client(key=API_KEY)
    distance_matrix = gm.distance_matrix(origin, destination, mode='driving', units='metric')

    if distance_matrix['status'] == 'OK':
        return {'time': distance_matrix['rows'][0]['elements'][0]['duration']['value'],
                'distance': distance_matrix['rows'][0]['elements'][0]['distance']['value']}
    else:
        return {'Error': 'Something went wrong'}
