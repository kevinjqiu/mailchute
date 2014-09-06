import bottle
import sqlalchemy
from mailchute import db
from mailchute.api.exception import NotFound, BadRequest
from mailchute.model import IncomingEmail, RawMessage
from mailchute.api.serializer import (
    response, IncomingEmailDTO, RawMessageDTO)


app = bottle.app()


app.route('/emails', ['OPTIONS'])(lambda: {})
@app.route('/emails', ['GET'])
@response('emails', IncomingEmailDTO)
def get_emails():
    inbox = bottle.request.query.get('inbox', None)
    if not inbox:
        raise BadRequest("'inbox' must be specified")
    emails = (
        db.session.query(IncomingEmail).filter_by(recipient=inbox).all()
    )
    return emails


app.route('/emails/<email_id:int>', ['OPTIONS'])(lambda *a, **kw: {})
@app.route('/emails/<email_id:int>', ['DELETE'])
@response('emails', None)
def delete_email(email_id):
    if not db.session.query(IncomingEmail).filter_by(id=email_id).count():
        raise NotFound

    model = db.session.query(IncomingEmail).filter_by(id=email_id).one()
    db.session.delete(model)
    db.session.commit()


app.route('/raw_messages/<raw_message_id>', ['OPTIONS'])(lambda *a, **kw: {})
@app.route('/raw_messages/<raw_message_id>', ['GET'])
@response('raw_messages', RawMessageDTO)
def get_raw_message(raw_message_id):
    try:
        return (
            db.session.query(RawMessage).join(IncomingEmail)
            .filter(RawMessage.raw_message_id == raw_message_id)
            .one()
        )
    except sqlalchemy.orm.exc.NoResultFound:
        raise NotFound()


@app.hook('after_request')
def enable_cors():
    ALLOWED_METHODS = 'PUT, GET, POST, DELETE, OPTIONS'
    ALLOWED_HEADERS = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Methods'] = ALLOWED_METHODS
    bottle.response.headers['Access-Control-Allow-Headers'] = ALLOWED_HEADERS
