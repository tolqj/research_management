"""
认证路由
处理用户登录、注册
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import schemas
from crud import user as crud_user
from utils.security import verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse, summary="用户注册")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    - 检查用户名和邮箱是否已存在
    - 创建新用户
    """
    # 检查用户名是否已存在
    if crud_user.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 检查邮箱是否已存在
    if user.email and crud_user.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被使用"
        )
    
    # 创建用户
    db_user = crud_user.create_user(db, user)
    return db_user


@router.post("/login", response_model=schemas.LoginResponse, summary="用户登录")
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录接口
    - 验证用户名和密码
    - 返回 JWT Token 和用户信息
    """
    # 查找用户
    user = crud_user.get_user_by_username(db, login_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 验证密码
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 生成 Token
    access_token = create_access_token(data={"user_id": user.id, "username": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
