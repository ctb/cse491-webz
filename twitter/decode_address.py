import urllib, urllib2, StringIO, json

def decodeAddressToCoordinates(address):
	urlParams = dict(address=address, sensor='false')
	
        url = 'http://maps.google.com/maps/api/geocode/json?' + \
	      urllib.urlencode(urlParams)
        response = urllib2.urlopen(url)
        responseBody = response.read()

	print 'GOT response:', responseBody

        body = StringIO.StringIO(responseBody)
        result = json.load(body)
	
        if 'status' not in result or result['status'] != 'OK':
                return None
        else:
                return {
                   'lat': result['results'][0]['geometry']['location']['lat'],
                   'lng': result['results'][0]['geometry']['location']['lng']
		   }  

if __name__ == '__main__':
	address = 'Constitution Ave NW & 10th St NW, Washington, DC'
	print decodeAddressToCoordinates(address)
