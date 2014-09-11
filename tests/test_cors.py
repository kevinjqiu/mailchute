from webtest import TestApp
from mailchute.api.app import app


app = TestApp(app)


def assert_correct_cors_headers(route):
    response = app.options(route, status=200)
    assert response.body == b'{}'
    assert response.headers['Access-Control-Allow-Headers'] == \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    assert response.headers['Access-Control-Allow-Methods'] == \
        'PUT, GET, POST, DELETE, OPTIONS'
    assert response.headers['Access-Control-Allow-Origin'] == '*'


def test_cors():
    routes = [
        '/emails/1',
        '/emails',
        '/raw_messages/cafebabe',
    ]
    for route in routes:
        yield assert_correct_cors_headers, route
