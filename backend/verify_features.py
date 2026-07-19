from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

register = client.post('/auth/register', json={'name': 'Casey', 'email': 'casey@example.com', 'password': 'secret123'})
print('register', register.status_code, register.json())
login = client.post('/auth/login', json={'email': 'casey@example.com', 'password': 'secret123'})
print('login', login.status_code, login.json())
token = login.json()['access_token']
symptom = client.post('/analysis/symptoms', json={'symptoms': 'I have fever, headache and cough'}, headers={'Authorization': f'Bearer {token}'})
print('symptom', symptom.status_code, symptom.json())
report = client.post('/analysis/report', files={'file': ('report.txt', b'Blood pressure 165/95, cholesterol elevated, acute symptoms', 'text/plain')}, headers={'Authorization': f'Bearer {token}'})
print('report', report.status_code, report.json())
history = client.get('/analysis/history', headers={'Authorization': f'Bearer {token}'})
print('history', history.status_code, history.json())
dashboard = client.get('/dashboard', headers={'Authorization': f'Bearer {token}'})
print('dashboard', dashboard.status_code, dashboard.json())
