import os
from logbook import Logger


logger = Logger(__name__)


def env(env_key, default):
    if env_key in os.environ:
        result = os.environ[env_key]
        logger.debug("Set {} from os.environ".format(env_key))
    else:
        result = default
        logger.debug("Set {} to default".format(env_key))
    return result


DB = {
    'url': env('DB_URL', 'sqlite:///mailchute.db'),
}

SMTPD = {
    'host': env('SMTPD_HOST', '0.0.0.0'),
    'port': env('SMTPD_PORT', 25),
}

API = {
    'host': env('API_HOST', '0.0.0.0'),
    'port': env('API_PORT', '8080'),
}

RECEIVER_DOMAIN = env('MAILCHUTE_RECEIVER_DOMAIN', None)
