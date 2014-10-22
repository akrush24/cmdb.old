from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
options = Table('options', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=100)),
    Column('type_id', INTEGER),
    Column('front_page', INTEGER),
    Column('description', VARCHAR(length=100)),
    Column('opttype', VARCHAR(length=10)),
    Column('user_visible', INTEGER),
    Column('requiared', INTEGER),
)

options = Table('options', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('type_id', Integer),
    Column('description', String(length=100)),
    Column('opttype', String(length=10)),
    Column('user_visible', Integer),
    Column('front_page', Integer),
    Column('required', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['options'].columns['requiared'].drop()
    post_meta.tables['options'].columns['required'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['options'].columns['requiared'].create()
    post_meta.tables['options'].columns['required'].drop()
