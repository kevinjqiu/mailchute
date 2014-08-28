from bottle import run


def main():
    import mailchute.api.resource as _
    run(host='localhost', port=8080)
