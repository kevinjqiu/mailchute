import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker


engine = sa.create_engine('sqlite:///mailchute.db')


Session = scoped_session(sessionmaker(bind=engine))

session = Session()
