# -*- coding: utf-8 -*-
"""
    sqlalchemy_seed
    ~~~~~~~~~~~~~~~

    `sqlalchemy_seed` is a seed library which provides initial data to
    database using SQLAlchemy.

    :copyright: (c) 2017 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
import os
import importlib
import json
import yaml

__version__ = '0.1.1'


def create_table(base, session=None):
    """Create table.

    :param base: `sqlalchemy.ext.declarative`
    :param session: `sqlalchemy.orm`
    """
    if session:
        base.metadata.create_all(bind=session.bind)
    else:
        base.metadata.create_all()


def drop_table(base, session):
    """Drop table.

    :param base: `sqlalchemy.ext.declarative`
    :param session: `sqlalchemy.orm`
    """
    session.expunge_all()
    session.remove()
    base.metadata.drop_all()


def load_fixture_files(paths, files):
    """Load fixture files.

    :param path: Path to fixtures
    :param files: Fixture file names
    """
    fixtures = []
    if not isinstance(paths, list):
        paths = [paths]

    for path in paths:
        for file in files:
            fixture_path = os.path.join(path, file)
            if not os.path.exists(fixture_path):
                continue

            with open(fixture_path, 'r') as f:
                if file.endswith('.yaml') or file.endswith('.yml'):
                    data = yaml.load(f)
                elif file.endswith('.json'):
                    data = json.loads(f)
                else:
                    continue
                fixtures.append(data)

    return fixtures


def _create_model_instance(fixture):
    """Create model instance.

    :param fixture: Fixtures
    """
    instances = []
    for data in fixture:
        if 'model' in data:
            module_name, class_name = data['model'].rsplit('.', 1)
            module = importlib.import_module(module_name)
            model = getattr(module, class_name)
            instance = model(**data['fields'])
            instances.append(instance)

    return instances


def load_fixtures(session, fixtures):
    """Load fixture.

    :param base: `sqlalchemy.ext.declarative`
    :param fixtures: Fixture files
    """
    instances = []
    for fixture in fixtures:
        _instances = _create_model_instance(fixture)
        for instance in _instances:
            instances.append(instance)

    try:
        session.add_all(instances)
        session.flush()
        session.commit()
    except:
        session.rollback()
        raise
