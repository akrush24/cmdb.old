from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
dict = Table('dict', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
)

dict_val = Table('dict_val', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('dict_id', Integer),
    Column('name', String(length=255)),
)

options = Table('options', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('type_id', Integer),
)

types = Table('types', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=24)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['dict'].create()
    post_meta.tables['dict_val'].create()
    post_meta.tables['options'].create()
    post_meta.tables['types'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['dict'].drop()
    post_meta.tables['dict_val'].drop()
    post_meta.tables['options'].drop()
    post_meta.tables['types'].drop()
