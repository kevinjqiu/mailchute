from os import environ


def env(env_key, default):
    return environ.get(env_key, default)


DB = {
    'url': env('DB_URL', 'sqlite:///mailchute.db'),
}

SMTPD = {
    'host': env('SMTPD_HOST', '0.0.0.0'),
    'port': env('SMTPD_PORT', 25),
}

API = {
    'host': env('API_HOST', 'localhost'),
    'port': env('API_PORT', '8080'),
}
