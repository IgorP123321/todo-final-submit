from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from typing import List, Optional
DATABASE_URL = "sqlite:///./moja_baza.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

class TaskDB(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()


@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    if db.query(UserDB).filter((UserDB.username == user.username) | (UserDB.email == user.email)).first():
        raise HTTPException(status_code=400, detail="Użytkownik lub e-mail już istnieje")
    new_user = UserDB(username=user.username, email=user.email, password_hash=pwd_context.hash(user.password))
    db.add(new_user)
    db.commit()
    return {"status": "success"}

@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Błędne dane")
    return {"user_id": db_user.id, "username": db_user.username}

@app.get("/tasks/{u_id}")
def get_tasks(u_id: int, db: Session = Depends(get_db)):
    return db.query(TaskDB).filter(TaskDB.owner_id == u_id).all()

@app.post("/tasks/{u_id}")
def add_task(u_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskDB(**task.dict(), owner_id=u_id)
    db.add(new_task)
    db.commit()
    return {"status": "success"}

@app.delete("/tasks/{t_id}")
def delete_task(t_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == t_id).first()
    if not task: raise HTTPException(status_code=404)
    db.delete(task)
    db.commit()
    return {"status": "deleted"}