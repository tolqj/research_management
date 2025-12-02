"""
用户 CRUD 操作
"""
from sqlalchemy.orm import Session
from typing import Optional, List
import models
import schemas
from utils.security import hash_password


def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """根据ID获取用户"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """根据用户名获取用户"""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """根据邮箱获取用户"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    role: Optional[models.UserRole] = None,
    college: Optional[str] = None
) -> List[models.User]:
    """获取用户列表"""
    query = db.query(models.User)
    
    if role:
        query = query.filter(models.User.role == role)
    if college:
        query = query.filter(models.User.college == college)
    
    return query.offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """创建用户"""
    db_user = models.User(
        username=user.username,
        password_hash=hash_password(user.password),
        name=user.name,
        role=user.role,
        title=user.title,
        college=user.college,
        email=user.email,
        phone=user.phone,
        research_field=user.research_field,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """更新用户信息"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """删除用户"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def change_password(db: Session, user_id: int, new_password: str) -> bool:
    """修改密码"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db_user.password_hash = hash_password(new_password)
    db.commit()
    return True
