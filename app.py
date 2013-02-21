#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse

class SimpleApp(object):
    def __call__(self, environ, start_response):
        status = '200 OK'

        path = environ['PATH_INFO']

        if path == '/':
            content_type = 'text/html'
            data = """\
Visit:
<a href='content'>a file</a>,
<a href='error'>an error</a>,
<a href='helmet'>an image</a>,
<a href='somethingelse'>something else</a>, or
<a href='form'>a form...</a>
<p>
<img src='/helmet'>
"""
        elif path == '/content':
            content_type = 'text/html'
            data = open('somefile.html').read()
        elif path == '/error':
            status = "404 Not Found"
            content_type = 'text/html'
            data = "Couldn't find your stuff."
        elif path == '/helmet':
            content_type = 'image/gif'
            data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()
        elif path == '/form':
            content_type = 'text/html'
            data = form()
        elif path == '/recv':
            formdata = environ['QUERY_STRING']
            results = urlparse.parse_qs(formdata)

            firstname = results['firstname'][0]
            lastname = results['lastname'][0]

            content_type = 'text/html'
            data = "First name: %s; last name: %s.  <a href='./'>return to index</a>" % (firstname, lastname)
        else:
            content_type = 'text/plain'
            data = "Hello, world; got path request %s" % environ['PATH_INFO']
        
        headers = [('Content-type', content_type)]
        start_response(status, headers)

        return [data]

def form():
    return """
<form action='recv'>
Your first name? <input type='text' name='firstname' size'20'>
Your last name? <input type='text' name='lastname' size='20'>
<input type='submit'>
</form>
"""

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
