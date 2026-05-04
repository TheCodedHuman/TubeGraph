# In FastAPI we create a file in which we write authentication based endpoint
# which gets paired later in other files with services requiring login tokens

# Imports
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, get_db_session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.core.security import get_password_hash, verify_password, create_access_token


# Mini-Router for "this" specific file
router = APIRouter()


# Routes
# The POST endpoint, returns the safe "UserResponse" schema
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db_session)):
    
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


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_session)):
    """The Bouncer at the door verifying credentials and handing out wristbands"""

    # (OAuth2 forms always use the field name 'username', but we will ask users to type their email into it)
    user = db.query(User).filter(User.email == form_data.username).first()          # 1. Look up the user by Email

    if not user or not verify_password(form_data.password, user.password_hash):     # 2. Check if user exists AND if the password matches the hash
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # "sub" stands for Subject. It is an official industry standard for JWTs
    access_token = create_access_token(data={"sub": user.email})                    # 3. Forge the wristband! We embed the user's email inside the token so we know who they are later      
    
    return {                                                                        # 4. Return the wristband to the user, and not the bouncer itself ;)
        "access_token": access_token,
        "token_type": "bearer"
    }
