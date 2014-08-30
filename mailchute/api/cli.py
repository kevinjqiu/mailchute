import bottle
from mailchute import settings
from mailchute.api.resource import app


def main():
    import mailchute.api.resource as _
    bottle.run(
        app,
        host=settings.API['host'],
        port=settings.API['port'],
    )
