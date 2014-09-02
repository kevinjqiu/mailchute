import uuid
import sqlalchemy as sa
import datetime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class RawMessage(Base):
    __tablename__ = 'raw_message'

    raw_message_id = sa.Column(sa.String(32), primary_key=True)
    message = sa.Column(sa.Text)

    def __init__(self, *args, **kwargs):
        kwargs['raw_message_id'] = uuid.uuid4().hex
        super(RawMessage, self).__init__(*args, **kwargs)


class IncomingEmail(Base):
    __tablename__ = 'incoming_email'

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now())
    sender = sa.Column(sa.String)
    recipient = sa.Column(sa.String)
    subject = sa.Column(sa.String)
    raw_message_id = sa.Column(
        sa.String(32), sa.ForeignKey('raw_message.raw_message_id'))
    raw_message = sa.orm.relationship(RawMessage)
