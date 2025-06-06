# StudyHub Database Migration Environment Configuration
# This file configures the Alembic migration environment for the StudyHub Flask application.
# It handles both online and offline migration modes and integrates with Flask-SQLAlchemy.

# Core imports for migration functionality
import logging  # Logging system for migration operations
from logging.config import fileConfig  # Configuration loader for logging

from flask import current_app  # Access to current Flask application context

from alembic import context  # Alembic migration context manager

# Configuration object setup
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config  # Load Alembic configuration from alembic.ini

# Logging configuration setup
# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)  # Configure Python logging from alembic.ini
logger = logging.getLogger('alembic.env')  # Create logger for this environment

# Database engine retrieval function
# Handles compatibility between different Flask-SQLAlchemy versions
def get_engine():
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()  # Get engine for older versions
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine  # Get engine for newer versions


# Database URL retrieval function
# Extracts database connection URL from the engine
def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')  # Render URL as string and escape % characters
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')  # Fallback URL conversion


# Database configuration setup
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())  # Set database URL in config
target_db = current_app.extensions['migrate'].db  # Get Flask-Migrate database instance

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# Metadata retrieval function
# Handles compatibility between different Flask-SQLAlchemy versions
def get_metadata():
    if hasattr(target_db, 'metadatas'):  # Check if multi-database support exists
        return target_db.metadatas[None]  # Return default database metadata
    return target_db.metadata  # Return single database metadata


# Offline migration function
# Runs database migrations without connecting to the database
def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")  # Get database URL from config
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True  # Configure migration context
    )

    with context.begin_transaction():  # Start migration transaction
        context.run_migrations()  # Execute migration scripts


# Online migration function  
# Runs database migrations with active database connection
def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # this callback is used to prevent an auto-migration from being generated
    # when there are no changes to the schema
    # reference: http://alembic.zzzcomputing.com/en/latest/cookbook.html
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):  # Check if autogenerate is enabled
            script = directives[0]  # Get first migration script
            if script.upgrade_ops.is_empty():  # Check if no schema changes detected
                directives[:] = []  # Clear directives to prevent empty migration
                logger.info('No changes in schema detected.')  # Log no changes message

    conf_args = current_app.extensions['migrate'].configure_args  # Get Flask-Migrate configuration
    if conf_args.get("process_revision_directives") is None:  # Check if callback not set
        conf_args["process_revision_directives"] = process_revision_directives  # Set callback

    connectable = get_engine()  # Get database engine connection

    with connectable.connect() as connection:  # Establish database connection
        context.configure(
            connection=connection,  # Set database connection
            target_metadata=get_metadata(),  # Set target metadata
            **conf_args  # Apply additional configuration arguments
        )

        with context.begin_transaction():  # Start migration transaction
            context.run_migrations()  # Execute migration scripts


# Migration execution controller
# Determines whether to run online or offline migrations
if context.is_offline_mode():  # Check if running in offline mode
    run_migrations_offline()  # Execute offline migrations
else:
    run_migrations_online()  # Execute online migrations
