"""
This module sets up the database configuration for the URL shortener application.

It includes the creation of the SQLAlchemy engine, session maker, and base class for ORM models.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

# Retrieve the database URL from the settings
db_url = get_settings().db_url

# Create a SQLAlchemy engine with the retrieved database URL
# 'connect_args={"check_same_thread": False}' is specific to SQLite and allows multithreading
engine = create_engine(db_url, connect_args={"check_same_thread": False})
"""
SQLAlchemy engine for connecting to the database.

The engine is configured with the database URL from the settings and 
connect_args for SQLite to allow multithreading.
"""

# Create a configured "Session" class
# This session factory will be used to create new session objects when interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
SQLAlchemy session factory for creating database sessions.

The session factory is configured with the engine, and the sessions do not 
autocommit or autoflush by default.
"""

# Create a base class for declarative class definitions
# All ORM models should inherit from this base class to use SQLAlchemy's ORM features
Base = declarative_base()
"""
Base class for SQLAlchemy ORM models.

All ORM models should inherit from this base class.
"""
