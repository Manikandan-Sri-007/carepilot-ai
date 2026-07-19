from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.database as database_module
from app.main import app

engine = create_engine(
    'sqlite:///:memory:',
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)
database_module.engine = engine
database_module.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database_module.Base.metadata.create_all(bind=engine)


def override_get_db():
    db = database_module.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[database_module.get_db] = override_get_db
client = TestClient(app)

response = client.post(
    '/auth/register',
    json={'name': 'Alicia', 'email': 'alicia@example.com', 'password': 'secret123'},
)
print('STATUS', response.status_code)
print(response.text)

login_response = client.post(
    '/auth/login',
    json={'email': 'alicia@example.com', 'password': 'secret123'},
)
print('LOGIN_STATUS', login_response.status_code)
print(login_response.text)
