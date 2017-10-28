# -*- coding: utf-8 -*-
"""
    sqlalchemy_seed.test_sqlalchmy_seed
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Test for sqlalchemy_seed.


    :copyright: (c) 2017 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""

import os
from unittest import TestCase

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy_seed import (
    create_table,
    drop_table,
    load_fixtures,
    load_fixture_files,
)
from sqlalchemy_seed.mixin import SeedMixin


engine = create_engine('sqlite://', convert_unicode=True)
Base = declarative_base()
Base.metadata.bind = engine
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(Session)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    age = Column(Integer(), nullable=True)

    def __repr__(self):
        return 'Account(id={0}, first_name={1}, last_name={2}, age={3})'.format(
            self.id, self.first_name, self.last_name, self.age,
        )


class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    image = Column(String(120), unique=True)

    account = relationship(
        'Account',
        backref='images',
        primaryjoin='Account.id==Picture.account_id',
        lazy='joined',
    )

    def __init__(self, account_id=None, image=None):
        self.account_id = account_id
        self.image = image

    def __repr__(self):
        return 'Picture(id={0}, account_id={1}, image={2})'.format(
            self.id,
            self.account,
            self.image,
        )


class TestFixtures(TestCase):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')

    def test_load_fixture_files(self):
        fixtures = load_fixture_files(self.path, ['accounts.yaml'])
        self.assertTrue(isinstance(fixtures[0], list))

    def test_create_table(self):
        create_table(Base)
        accounts = session.query(Account).all()
        self.assertEqual(len(accounts), 0)

    def test_drop_table(self):
        create_table(Base)
        drop_table(Base, session)
        with self.assertRaises(OperationalError):
            session.query(Account).all()

    def test_load_fixture(self):
        create_table(Base)
        fixtures = load_fixture_files(self.path, ['accounts.yaml'])
        load_fixtures(session, fixtures)
        accounts = session.query(Account).all()
        self.assertEqual(len(accounts), 2)

        drop_table(Base, session)

    def test_load_fixtures(self):
        create_table(Base)
        fixtures = load_fixture_files(
            self.path, ['accounts.yaml', 'pictures.yaml'],
        )
        load_fixtures(session, fixtures)
        accounts = session.query(Account).all()
        self.assertEqual(len(accounts), 2)
        pictures = session.query(Picture).all()
        self.assertEqual(len(pictures), 4)

        drop_table(Base, session)

    def test_load_fixture_by_wrong_order(self):
        # Picture has relationship to Account.
        # Model instances are added by `session.add_all()`.
        # So, it does not fail.
        create_table(Base)
        fixtures = load_fixture_files(
            self.path, ['pictures.yaml', 'accounts.yaml'],
        )
        load_fixtures(session, fixtures)
        accounts = session.query(Account).all()
        self.assertEqual(len(accounts), 2)
        pictures = session.query(Picture).all()
        self.assertEqual(len(pictures), 4)

        drop_table(Base, session)


class TestSeedMixin(SeedMixin, TestCase):
    base = Base
    session = session
    fixtures = ['accounts.yaml', 'pictures.yaml']
    fixtures_paths = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'fixtures',
    )

    def test_create_seed_data(self):
        accounts = session.query(Account).all()
        self.assertEqual(len(accounts), 2)

        pictures = session.query(Picture).all()
        self.assertEqual(len(pictures), 4)


class TestSeedMixiSetUp(SeedMixin, TestCase):
    base = Base
    session = session
    fixtures = ['accounts.yaml', 'pictures.yaml']
    fixtures_paths = 'fixtures'
    fixtures_setup_class = False

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_setup_and_teardown_not_called(self):
        with self.assertRaises(OperationalError):
            session.query(Account).all()


class TestSeedMixinSetUpClass(SeedMixin, TestCase):
    base = Base
    session = session
    fixtures = ['accounts.yaml', 'pictures.yaml']
    fixtures_paths = 'fixtures'
    fixtures_setup_class = True

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_setup_class_and_teardown_class_not_called(self):
        with self.assertRaises(OperationalError):
            session.query(Account).all()
