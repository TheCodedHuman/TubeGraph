# In FastAPI we create a file in which we write authentication based endpoint
# which gets paired later in other files with services requiring login tokens

# Imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash


# Mini-Router for "this" specific file
router = APIRouter()


# Defined
def get_db():
    """This opens a database connection for the request, and safely closes it after"""
    db = SessionLocal()
    try: yield db
    finally: db.close()


# Routes
# The POST endpoint, returns the safe "UserResponse" schema
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    
    # 1. Check if the email already exists (or taken)
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system."
        )
    
    # 2. Scramble the raw password using the our core security function
    hashed_pw = get_password_hash(user_in.password)

    # 3. Create the SQLAlchemy Vault Object
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        password_hash=hashed_pw
    )

    # 4. Save it to the PostgreSQL hard drive
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 5. Return it to the frontend. Pydantic will automatically strip the password out (response_model parameter did this magic here)
    return db_user

