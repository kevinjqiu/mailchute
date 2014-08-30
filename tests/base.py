from mailchute import db


class BaseTestCase(object):
    IGNORED_TABLES = set([
        'alembic_version',
    ])

    def reset_tables(self):
        for table_name in db.engine.table_names():
            if table_name not in self.IGNORED_TABLES:
                db.engine.execute("DELETE FROM {0}".format(table_name))

    def teardown(self):
        self.reset_tables()
