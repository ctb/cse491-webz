#! /usr/bin/env python
import sys
import simplejson
import urllib2

class MagicFunction(object):
    def __init__(self, base, name):
        self.url = base
        self.name = name

    def __call__(self, *params):
        return call_remote(self.url, self.name, params, 1)

class JSON_RPC_Magic(object):
    def __init__(self, base_http_url):
        self.url = base_http_url + 'rpc'
        self.methods = set(['hello', 'add'])

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        if name not in self.__dict__['methods']:
            return None

        fn = MagicFunction(self.url, name)
        self.__dict__[name] = fn

        return fn

def call_remote(base, method, params, id):
    # encode things in a dict that is then converted into JSON
    d = dict(method=method, params=params, id=id)
    encoded = simplejson.dumps(d)

    # specify appropriate content-type
    headers = { 'Content-Type' : 'application/json' }

    # call remote server
    req = urllib2.Request(base, encoded, headers)

    # get response
    response_stream = urllib2.urlopen(req)
    json_response = response_stream.read()

    # decode response
    response = simplejson.loads(json_response)

    # return result
    return response['result']

if __name__ == '__main__':
    magic = JSON_RPC_Magic(sys.argv[1])
    print magic.hello()
    print magic.add(2, 3)
