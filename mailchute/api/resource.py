from bottle import route
from mailchute import db
from mailchute.model import IncomingEmail, RawMessage
from mailchute.api.serializer import (
    ResponseDTO, IncomingEmailDTO, RawMessageDTO)


@route('/inbox/:recipient/')
def get_incoming_emails(recipient):
    results = (
        db.session.query(IncomingEmail).filter_by(recipient=recipient).all()
    )
    return ResponseDTO('incoming_emails', list(map(IncomingEmailDTO, results)))


@route('/inbox/:recipient/raw_message/:raw_message_id')
def get_raw_message(recipient, raw_message_id):
    result = (
        db.session.query(RawMessage).join(IncomingEmail)
        .filter(IncomingEmail.recipient == recipient)
        .filter(RawMessage.raw_message_id == raw_message_id)
        .one()
    )
    return ResponseDTO('raw_messages', list(map(RawMessageDTO, [result])))
