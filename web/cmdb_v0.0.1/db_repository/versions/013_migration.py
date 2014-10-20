from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('email', VARCHAR(length=120)),
    Column('name', VARCHAR(length=50)),
    Column('password', VARCHAR(length=255)),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('login', String(length=50)),
    Column('full_name', String(length=150)),
    Column('email', String(length=120)),
    Column('password', String(length=255)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['name'].drop()
    post_meta.tables['users'].columns['full_name'].create()
    post_meta.tables['users'].columns['login'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['name'].create()
    post_meta.tables['users'].columns['full_name'].drop()
    post_meta.tables['users'].columns['login'].drop()
