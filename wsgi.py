from app import main

def application(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    if path == 'health':
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b"OK"]
    else:
        main()
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b"Hello World!"]