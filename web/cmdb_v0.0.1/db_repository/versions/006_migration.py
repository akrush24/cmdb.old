from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
workflow = Table('workflow', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=250)),
    Column('step', Integer),
)

workflow_s = Table('workflow_s', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=250)),
)

types = Table('types', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=24)),
    Column('workflow', Integer),
    Column('desc', String(length=244)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['workflow'].create()
    post_meta.tables['workflow_s'].create()
    post_meta.tables['types'].columns['workflow'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['workflow'].drop()
    post_meta.tables['workflow_s'].drop()
    post_meta.tables['types'].columns['workflow'].drop()
