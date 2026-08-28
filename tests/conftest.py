import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.core.config.env_config import EnvConfig
from app.core.data.source.local.base import Base
from app.core.providers.db import get_db_session
from app.core.providers.env_config import get_env_config
from app.features.admin.country.infrastructure.models.country_model import CountryModel
from app.features.auth.infrastructure.models.audit_log_model import AuditLogModel
from app.features.auth.infrastructure.models.user_model import UserModel
from app.main import app


@pytest.fixture(scope="session")
def test_config() -> EnvConfig:
    return EnvConfig(
        db_user="test",
        db_password="testpassword",
        db_name="test_db",
        db_port=5432,
        db_host="localhost",
        jwt_secret_key="test-secret-key-for-unit-testing-purposes-123",
        jwt_algorithm="HS256",
        access_token_expire_minutes=15,
        refresh_token_expire_days=7,
        bcrypt_rounds=4,  # Fast rounds for test performance
    )


@pytest.fixture(scope="function")
def db_session() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session, test_config: EnvConfig) -> TestClient:
    def override_get_db_session():
        yield db_session

    def override_get_env_config():
        return test_config

    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_env_config] = override_get_env_config

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
