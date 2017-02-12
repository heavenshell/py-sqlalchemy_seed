# -*- coding: utf-8 -*-
"""
    sqlalchemy_seed.seed_mixin
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Mixin class for unittest.


    :copyright: (c) 2017 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from . import (
    create_table,
    drop_table,
    load_fixtures,
    load_fixture_files,
)


class SeedMixin(object):
    base = None
    session = None
    fixtures = []
    fixtures_setup_class = False
    fixtures_paths = None

    def _create_fixtures(self):
        if self.base is None:
            return
        if self.session is None:
            return
        if self.fixtures_paths is None:
            return

        create_table(self.base, self.session)
        fixtures = load_fixture_files(self.fixtures_paths, self.fixtures)
        load_fixtures(self.session, fixtures)

    def _drop_fixtures(self):
        drop_table(self.base, self.session)

    @classmethod
    def setUpClass(cls):
        if cls.fixtures_setup_class is True:
            cls._create_fixtures(cls)

    @classmethod
    def teatDownClass(cls):
        if cls.fixtures_setup_class is True:
            cls._drop_fixtures(cls)

    def setUp(self):
        if self.fixtures_setup_class is True:
            return
        self._create_fixtures()

    def tearDown(self):
        if self.fixtures_setup_class is True:
            return
        self._drop_fixtures()
