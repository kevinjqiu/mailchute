import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker


engine = sa.create_engine(
    'postgresql+psycopg2://mailchute:mailchute@localhost/mailchute')


Session = scoped_session(sessionmaker(bind=engine))

session = Session()
