# shortener_app/test_database.py

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from shortener_app.database import Base, SessionLocal
from shortener_app.models import URL

# Create an in-memory SQLite database for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create a new engine instance for the test database
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a new sessionmaker instance for the test database
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db_engine():
    """
    Fixture for creating a new database engine for the test module.
    """
    # Create the database and the tables
    Base.metadata.create_all(bind=engine)
    yield engine
    # Drop the tables and remove the database file after tests are done
    Base.metadata.drop_all(bind=engine)
    if os.path.exists('./test.db'):
        os.remove('./test.db')

@pytest.fixture(scope="module")
def db_session(db_engine):
    """
    Fixture for creating a new database session for each test module.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session  # Provide the fixture value
    
    session.close()
    transaction.rollback()
    connection.close()

def test_create_url(db_session):
    """
    Test creating a new URL entry in the database.
    """
    new_url = URL(target_url="https://example.com")
    db_session.add(new_url)
    db_session.commit()
    
    assert new_url.id is not None
    assert new_url.target_url == "https://example.com"
    assert new_url.is_active is True
    assert new_url.clicks == 0

def test_read_url(db_session):
    """
    Test reading a URL entry from the database.
    """
    url = db_session.query(URL).filter_by(target_url="https://example.com").first()
    
    assert url is not None
    assert url.target_url == "https://example.com"
    assert url.is_active is True
    assert url.clicks == 0

def test_update_url(db_session):
    """
    Test updating a URL entry in the database.
    """
    url = db_session.query(URL).filter_by(target_url="https://example.com").first()
    url.clicks += 1
    db_session.commit()
    
    updated_url = db_session.query(URL).filter_by(target_url="https://example.com").first()
    assert updated_url.clicks == 1

def test_delete_url(db_session):
    """
    Test deleting a URL entry from the database.
    """
    url = db_session.query(URL).filter_by(target_url="https://example.com").first()
    db_session.delete(url)
    db_session.commit()
    
    deleted_url = db_session.query(URL).filter_by(target_url="https://example.com").first()
    assert deleted_url is None
