from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, VARCHAR, TIMESTAMP, ForeignKey

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', VARCHAR, nullable=True),
    Column('last_name', VARCHAR, nullable=True),
    Column('username', VARCHAR, unique=True, nullable=False)
)

news = Table(
    'news',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('topic', VARCHAR, nullable=True),
    Column('main_text', VARCHAR, nullable=False),
    Column('image_url', VARCHAR, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow, nullable=False),
    Column('updated_at', TIMESTAMP, nullable=True),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
)
