import bottle
import sqlalchemy
from mailchute import db
from mailchute.api.exception import NotFound
from mailchute.model import IncomingEmail, RawMessage
from mailchute.api.serializer import (
    response, ResponseDTO, IncomingEmailDTO, RawMessageDTO)


@bottle.route('/inbox/<recipient>/')
@response('incoming_emails', IncomingEmailDTO)
def get_incoming_emails(recipient):
    return (
        db.session.query(IncomingEmail).filter_by(recipient=recipient).all()
    )


@bottle.route('/inbox/<recipient>/raw_message/<raw_message_id>')
@response('raw_messages', RawMessageDTO)
def get_raw_message(recipient, raw_message_id):
    try:
        return (
            db.session.query(RawMessage).join(IncomingEmail)
            .filter(IncomingEmail.recipient == recipient)
            .filter(RawMessage.raw_message_id == raw_message_id)
            .one()
        )
    except sqlalchemy.orm.exec.NoResultFound as e:
        raise NotFound()


app = bottle.app()
