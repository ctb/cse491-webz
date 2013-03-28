"""
Use the Twitter API to reverse geocode
"""

import urllib, json, pprint

params = urllib.urlencode(dict(lat=37.76893497, long=-122.42284884))

u = urllib.urlopen('https://api.twitter.com/1/geo/reverse_geocode.json?' + \
                   params)
j = json.load(u)
pprint.pprint(j)
