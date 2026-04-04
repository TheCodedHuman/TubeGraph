# Project Dependencies
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os
import sys


# Defined
def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Adding backend/ folder to the Python's path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Load the .env file from the root folder
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
from app.db.session import Base, SAFE_DATABASE_URL
from app.models.user import User
from app.models.flowchart import Flowchart
from app.models.userlibrary import UserLibrary


# target_metadata = mymodel.Base.metadata
# target_metadata = None
target_metadata = Base.metadata


# Components that will help construct the database url for the container (earlier it was just for windows)
db_user = os.getenv("POSTGRES_CONTAINER")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB")
db_server = os.getenv("POSTGRES_SERVER", "db")

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# configparser has a quirk: it thinks '%' means a variable. 
# So we escape our URL-encoded password (%40) to %%40 "just for Alembic"!
alembic_db_url = SAFE_DATABASE_URL.replace('%', '%%')
config.set_main_option("sqlalchemy.url", alembic_db_url)                                   


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
