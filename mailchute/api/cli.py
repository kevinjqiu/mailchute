import bottle
from mailchute import settings
from mailchute.api.resource import app


def main():
    import mailchute.api.resource as _
    bottle.run(
        app,
        settings.API['host'],
        settings.API['port'],
    )
