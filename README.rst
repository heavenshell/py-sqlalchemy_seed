sqlalchemy_seed
----------------

.. image:: https://travis-ci.org/heavenshell/py-sqlalchemy_seed.svg?branch=master
    :target: https://travis-ci.org/heavenshell/py-sqlalchemy_seed

`sqlalchemy_seed` is a seed library which provides initial data to database using SQLAlchemy.

`sqlalchemy_seed` is similar to `Django fixtures <https://docs.djangoproject.com/ja/1.10/howto/initial-data/>`_.

Installation
============

.. code::

  pip install sqlalchemy_seed

Adding seed
===========

.. code::

  /myapp
    __init__.py
    models.py
    /fixtures
      accounts.yaml

Model file.

.. code:: python

  # -*- coding: utf-8 -*-

  from sqlalchemy import create_engine
  from sqlalchemy.exc import OperationalError
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy.orm import scoped_session, sessionmaker, relationship
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


Seed code.

.. code:: python

  # -*- coding: utf-8 -*-

  from sqlalchemy_seed import (
      create_table,
      drop_table,
      load_fixtures,
      load_fixture_files,
  )
  from myapp.models import Base, session


  def main():
      path = '/path/to/fixtures'
      fixtures = load_fixture_files(path, ['accounts.yaml'])
      load_fixtures(session, fixtures)


  if __name__ == '__main__':
      main()

Seed file.

.. code::

  - model: myapp.models.Account
    id: 1
    fields:
      first_name: John
      last_name: Lennon
      age: 20

  - model: myapp.models.Account
    id: 2
    fields:
      first_name: Paul
      last_name: McCartney
      age: 21

LICENSE
=======
NEW BSD LICENSE.
