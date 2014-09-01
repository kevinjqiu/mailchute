import sqlalchemy as sa
from mailchute import settings
from sqlalchemy.orm import scoped_session, sessionmaker
from logbook import Logger


logger = Logger(__name__)
logger.info("DB_URL: {}".format(settings.DB['url']))

engine = sa.create_engine(settings.DB['url'])

Session = scoped_session(sessionmaker(bind=engine))

session = Session()
logger.debug("Session created")
