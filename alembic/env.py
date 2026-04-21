from logging.config import fileConfig
from dotenv import load_dotenv
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.database import Base
from app.models import User, Project, Board, Consumer

# this is the Alembic Config object
config = context.config

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# 🔧 NEW: load DATABASE_URL from environment (Docker ready)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# metadata for autogenerate
target_metadata = Base.metadata


# Custom filters
def include_object(object, name, type_, reflected, compare_to):
    # Ignore partial unique index (manually added)
    if type_ == "index" and name == "unique_root_per_project":
        return False
    return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_object=include_object,  # 🔧 ADD THIS
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,  # 🔧 ADD THIS
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()