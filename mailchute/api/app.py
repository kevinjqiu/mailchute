import bottle
from mailchute.api import resource


def _route(app, uri, methods, handler):
    app.route(uri, ['OPTIONS'])(lambda *a, **kw: {})
    app.route(uri, methods)(handler)


def create_app():
    app = bottle.app()
    _route(app, '/emails', ['GET'], resource.get_emails)
    _route(
        app, '/emails/<email_id:int>', ['DELETE'],
        resource.delete_email)
    _route(
        app, '/raw_messages/<raw_message_id>', ['GET'],
        resource.get_raw_message)

    @app.hook('after_request')
    def enable_cors():
        ALLOWED_METHODS = 'PUT, GET, POST, DELETE, OPTIONS'
        ALLOWED_HEADERS = \
            'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        bottle.response.headers['Access-Control-Allow-Origin'] = '*'
        bottle.response.headers['Access-Control-Allow-Methods'] = ALLOWED_METHODS
        bottle.response.headers['Access-Control-Allow-Headers'] = ALLOWED_HEADERS

    return app


app = create_app()
