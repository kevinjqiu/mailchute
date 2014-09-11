import bottle
from mailchute import settings
from mailchute.api.app import app


def main():  # pragma: no cover
    bottle.run(
        app,
        host=settings.API['host'],
        port=settings.API['port'],
    )
