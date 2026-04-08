from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.database import SessionLocal
from app.db.models import User
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import hash_password, verify_password, create_access_token
from app.core.token_blacklist import blacklist_token

router = APIRouter(prefix="/auth")


security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.user_id == req.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        user_id=req.user_id,
        password=hash_password(req.password)
    )
    db.add(user)
    db.commit()

    return {"message": "User registered successfully"}


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == req.user_id).first()
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.user_id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    blacklist_token(token)
    return {"message": "Logged out successfully"}