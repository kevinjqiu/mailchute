import bottle
import sqlalchemy
import datetime

from mailchute import db
from mailchute.api.exception import NotFound, BadRequest
from mailchute.model import IncomingEmail, RawMessage
from mailchute.api.serializer import (
    response, IncomingEmailDTO, RawMessageDTO)


@response('emails', IncomingEmailDTO)
def get_emails():
    inbox = bottle.request.query.get('inbox', None)
    if not inbox:
        raise BadRequest("'inbox' must be specified")
    emails = (
        db.session.query(IncomingEmail)
        .filter_by(recipient=inbox)
        .filter(IncomingEmail.deleted_at.is_(None))
        .all()
    )
    return emails


@response('emails', None)
def delete_email(email_id):
    if not db.session.query(IncomingEmail).filter_by(id=email_id).count():
        raise NotFound

    model = db.session.query(IncomingEmail).filter_by(id=email_id).one()
    model.deleted_at = datetime.datetime.now()
    db.session.add(model)
    db.session.commit()


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
