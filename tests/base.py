from mailchute.model import IncomingEmail, RawMessage
from mailchute import db


class FixtureCreatorMixin(object):
    def create_incoming_email(self, **kwargs):
        raw_message = kwargs.pop('raw_message', '')
        obj = IncomingEmail(**kwargs)
        obj.raw_message = RawMessage(message=raw_message)
        db.session.add(obj)
        db.session.commit()
        return obj


class BaseTestCase(FixtureCreatorMixin):
    IGNORED_TABLES = set([
        'alembic_version',
    ])

    def reset_tables(self):
        for table_name in db.engine.table_names():
            if table_name not in self.IGNORED_TABLES:
                db.engine.execute("DELETE FROM {0}".format(table_name))

    def teardown(self):
        self.reset_tables()
