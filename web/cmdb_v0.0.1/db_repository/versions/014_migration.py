from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
values = Table('values', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('option_id', INTEGER),
    Column('res_id', INTEGER),
    Column('value', VARCHAR(length=250)),
    Column('update_date', DATETIME),
)

value = Table('value', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('option_id', Integer),
    Column('res_id', Integer),
    Column('value', String(length=250)),
    Column('update_date', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['values'].drop()
    post_meta.tables['value'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['values'].create()
    post_meta.tables['value'].drop()
