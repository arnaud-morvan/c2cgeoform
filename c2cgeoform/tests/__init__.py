import os
import unittest
from pyramid import testing
from pyramid.paster import get_appsettings
from sqlalchemy import engine_from_config

from c2cgeoform.models import (DBSession, Base)


class DatabaseTestCase(unittest.TestCase):
    def setUp(self):  # noqa
        curdir = os.path.dirname(os.path.abspath(__file__))
        configfile = os.path.realpath(
            os.path.join(curdir, '../../development.ini'))
        settings = get_appsettings(configfile)
        engine = engine_from_config(settings, 'sqlalchemy.')
        DBSession.configure(bind=engine)

        from models_test import Person, EmploymentStatus, Tag  # noqa
        Base.metadata.create_all(engine)
        self.cleanup()

        # fill some test data into the `EmploymentStatus` and `Tags` table
        DBSession.add(EmploymentStatus(id=0, name='Worker'))
        DBSession.add(EmploymentStatus(id=1, name='Employee'))
        DBSession.add(EmploymentStatus(
            id=2, name='Self-employed and contractor'))
        DBSession.add(EmploymentStatus(id=3, name='Director'))
        DBSession.add(EmploymentStatus(id=4, name='Office holder'))

        DBSession.add(Tag(id=0, name='Tag A'))
        DBSession.add(Tag(id=1, name='Tag B'))
        DBSession.add(Tag(id=2, name='Tag C'))
        DBSession.add(Tag(id=3, name='Tag D'))
        DBSession.add(Tag(id=4, name='Tag E'))

    def tearDown(self):  # noqa
        self.cleanup()
        DBSession.remove()
        testing.tearDown()

    def cleanup(self):
        from models_test import Person, EmploymentStatus, Phone,\
            Tag, TagsForPerson
        DBSession.query(TagsForPerson).delete()
        DBSession.query(Tag).delete()
        DBSession.query(Phone).delete()
        DBSession.query(Person).delete()
        DBSession.query(EmploymentStatus).delete()
