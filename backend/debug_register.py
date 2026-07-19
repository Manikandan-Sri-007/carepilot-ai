import traceback
from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.database as database_module
from app.routes.auth import register
from app.schemas.auth import UserCreate

engine = create_engine('sqlite:///./carepilot.db', connect_args={'check_same_thread': False})
database_module.engine = engine
database_module.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = database_module.SessionLocal()
    try:
        yield db
    finally:
        db.close()

payload = UserCreate(name='DebugUser', email='debuguser@example.com', password='secret123')
request = Request({'type': 'http', 'method': 'POST', 'headers': [], 'query_string': b'', 'path': '/auth/register'})

db = database_module.SessionLocal()
try:
    result = register(payload=payload, request=request, db=db)
    print('RESULT', result)
except Exception as exc:
    print(type(exc).__name__, exc)
    traceback.print_exc()
finally:
    db.close()
