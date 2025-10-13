from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from bson import ObjectId

from app.core.config import settings
from app.core.responses import OutModel
from app.core.logging import get_logger
from app.db.mongodb import get_db

router = APIRouter()
logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str
    gender: Optional[str] = None
    dob: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    gender: Optional[str] = None
    dob: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None


class UpdateIn(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    dob: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None


async def get_user_from_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        db = get_db()
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        return user
    except Exception as e:
        logger.warning(f"Token decode error: {e}")
        return None


async def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization header")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization header")
    user = await get_user_from_token(token)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user


def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


@router.post("/register", response_model=OutModel)
async def register(payload: RegisterIn):
    db = get_db()
    existing = await db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    password_hash = pwd_context.hash(payload.password)
    doc = {
        "name": payload.name,
        "email": payload.email,
        "password_hash": password_hash,
        "role": "user",
        "gender": payload.gender,
        "dob": payload.dob,
        "height_cm": payload.height_cm,
        "weight_kg": payload.weight_kg,
        "activity_level": payload.activity_level,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    result = await db.users.insert_one(doc)
    user_out = UserOut(
        id=str(result.inserted_id),
        name=doc["name"],
        email=doc["email"],
        role=doc["role"],
        gender=doc.get("gender"),
        dob=doc.get("dob"),
        height_cm=doc.get("height_cm"),
        weight_kg=doc.get("weight_kg"),
        activity_level=doc.get("activity_level"),
    )
    return OutModel(status="success", message="Registered successfully", data=user_out.model_dump())


@router.post("/login", response_model=OutModel)
async def login(payload: LoginIn):
    db = get_db()
    user = await db.users.find_one({"email": payload.email})
    if not user or not pwd_context.verify(payload.password, user.get("password_hash", "")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_token({"sub": str(user["_id"])}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token({"sub": str(user["_id"])}, timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES))
    tokens = TokenOut(access_token=access_token, refresh_token=refresh_token)
    return OutModel(status="success", message="Login successful", data=tokens.model_dump())


@router.get("/me", response_model=OutModel)
async def me(user=Depends(get_current_user)):
    out = UserOut(
        id=str(user["_id"]),
        name=user.get("name"),
        email=user.get("email"),
        role=user.get("role", "user"),
        gender=user.get("gender"),
        dob=user.get("dob"),
        height_cm=user.get("height_cm"),
        weight_kg=user.get("weight_kg"),
        activity_level=user.get("activity_level"),
    )
    return OutModel(status="success", message="User profile", data=out.model_dump())


@router.patch("/update", response_model=OutModel)
async def update_profile(payload: UpdateIn, user=Depends(get_current_user)):
    db = get_db()
    updates = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if not updates:
        return OutModel(status="success", message="No changes", data={})
    updates["updated_at"] = datetime.utcnow()
    await db.users.update_one({"_id": user["_id"]}, {"$set": updates})
    user.update(updates)
    out = {
        "id": str(user["_id"]),
        "name": user.get("name"),
        "email": user.get("email"),
        "role": user.get("role", "user"),
        "gender": user.get("gender"),
        "dob": user.get("dob"),
        "height_cm": user.get("height_cm"),
        "weight_kg": user.get("weight_kg"),
        "activity_level": user.get("activity_level"),
    }
    return OutModel(status="success", message="Profile updated", data=out)
