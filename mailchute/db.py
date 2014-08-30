import sqlalchemy as sa
from mailchute import settings
from sqlalchemy.orm import scoped_session, sessionmaker


engine = sa.create_engine(settings.DB['url'])

Session = scoped_session(sessionmaker(bind=engine))

session = Session()
