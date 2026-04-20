import os
import pytest
from unittest import mock
from airflow.models import Variable

@pytest.fixture
def api_key():
    with mock.patch.dict(os.environ, "API_KEY": "MOCK_KEY1234"):
        yield Variable.get("API_KEY")

@pytest.fixture
def channel_handle():
    with mock.patch.dict(os.environ, "CHANNEL_HANDLE": "COMEDY_BITES"):
        yield Variable.get("CHANNEL_HANDLE")

@pytest.fixture
def mock_postgres_conn_vars():
    with mock.patch.dict(os.environ, {
        "POSTGRES_LOGIN": "mock_username",
        "POSTGRES_PASSWORD": "mock_password",
        "POSTGRES_HOST": "mock_host",
        "POSTGRES_PORT": "1234",
        "POSTGRES_SCHEMA": "mock_db_name"
    }):
        class MockPostgresConn:
            login = Variable.get("POSTGRES_LOGIN")
            password = Variable.get("POSTGRES_PASSWORD")
            host = Variable.get("POSTGRES_HOST")
            port = int(Variable.get("POSTGRES_PORT"))
            schema = Variable.get("POSTGRES_SCHEMA")

        yield MockPostgresConn()