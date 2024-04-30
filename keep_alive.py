from wsgiref.simple_server import make_server

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"I'm alive"]

# Create a simple WSGI server and run the application
with make_server('', 8080, application) as httpd:
    print("Serving on port 8080...")
    httpd.serve_forever()