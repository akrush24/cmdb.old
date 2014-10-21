from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
options = Table('options', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=100)),
    Column('type_id', Integer),
    Column('description', String(length=100)),
    Column('opttype', String(length=10)),
    Column('user_visible', Integer),
    Column('front_page', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['options'].columns['description'].create()
    post_meta.tables['options'].columns['opttype'].create()
    post_meta.tables['options'].columns['user_visible'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['options'].columns['description'].drop()
    post_meta.tables['options'].columns['opttype'].drop()
    post_meta.tables['options'].columns['user_visible'].drop()
