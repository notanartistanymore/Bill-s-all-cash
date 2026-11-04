import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.main import app

from app.config import settings
from app.database import Base, get_db


@pytest.fixture(scope="session")
def engine():
    if not settings.test_database_url:
        pytest.exit("TEST_DATABASE_URL is not set", returncode=1)
    engine = create_engine(settings.test_database_url)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def real_client(engine):
    session_factory = sessionmaker(bind=engine)

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE wallets"))
