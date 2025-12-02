"""
用户管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
from crud import user as crud_user
from utils.security import get_current_user, require_admin

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse, summary="获取当前用户信息")
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """获取当前登录用户的信息"""
    return current_user


@router.put("/me", response_model=schemas.UserResponse, summary="更新当前用户信息")
def update_current_user_info(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息"""
    updated_user = crud_user.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return updated_user


@router.post("/me/change-password", summary="修改密码")
def change_password(
    password_data: schemas.PasswordChange,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改当前用户密码"""
    from utils.security import verify_password
    
    # 验证旧密码
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码错误"
        )
    
    # 修改密码
    success = crud_user.change_password(db, current_user.id, password_data.new_password)
    if not success:
        raise HTTPException(status_code=500, detail="密码修改失败")
    
    return {"message": "密码修改成功"}


@router.get("/", response_model=List[schemas.UserResponse], summary="获取用户列表（管理员）")
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    role: Optional[models.UserRole] = None,
    college: Optional[str] = None,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """获取用户列表（仅管理员）"""
    users = crud_user.get_users(db, skip=skip, limit=limit, role=role, college=college)
    return users


@router.get("/{user_id}", response_model=schemas.UserResponse, summary="获取用户详情")
def get_user(
    user_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取指定用户的详细信息"""
    user = crud_user.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.post("/", response_model=schemas.UserResponse, summary="创建用户（管理员）")
def create_user(
    user: schemas.UserCreate,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """创建新用户（仅管理员）"""
    # 检查用户名是否已存在
    if crud_user.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查邮箱是否已存在
    if user.email and crud_user.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="邮箱已被使用")
    
    return crud_user.create_user(db, user)


@router.put("/{user_id}", response_model=schemas.UserResponse, summary="更新用户（管理员）")
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """更新用户信息（仅管理员）"""
    updated_user = crud_user.update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return updated_user


@router.delete("/{user_id}", summary="删除用户（管理员）")
def delete_user(
    user_id: int,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除用户（仅管理员）"""
    # 不能删除自己
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    success = crud_user.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return {"message": "用户删除成功"}
