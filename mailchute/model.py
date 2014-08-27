import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class IncomingEmailModel(Base):
    __tablename__ = 'incoming_email'
    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime)
    sender = sa.Column(sa.String)
    raw_message = sa.Column(sa.Text)
