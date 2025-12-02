"""
用户管理路由（符合等保二级要求）
包含完整的审计日志和密码策略
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
from crud import user as crud_user
from utils.security import get_current_user, require_admin
from utils.audit import AuditLogger, Timer
from utils.password_policy import PasswordPolicy

router = APIRouter()


@router.get("/me", response_model=schemas.UserResponse, summary="获取当前用户信息")
def get_current_user_info(current_user: models.User = Depends(get_current_user)):
    """获取当前登录用户的信息"""
    return current_user


@router.put("/me", response_model=schemas.UserResponse, summary="更新当前用户信息")
def update_current_user_info(
    user_update: schemas.UserUpdate,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息（含审计日志）"""
    timer = Timer()
    timer.start()
    
    try:
        # 收集变更
        changes = user_update.model_dump(exclude_unset=True)
        
        # 更新用户
        updated_user = crud_user.update_user(db, current_user.id, user_update)
        if not updated_user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 记录审计日志
        AuditLogger.log_update(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="user",
            resource_type="用户信息",
            resource_id=current_user.id,
            request=request,
            changes=changes
        )
        
        return updated_user
        
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="更新用户信息失败",
            module="user",
            request=request,
            status="FAILED",
            error_msg=str(e),
            duration=timer.elapsed_ms()
        )
        raise


@router.post("/me/change-password", summary="修改密码")
def change_password(
    password_data: schemas.PasswordChange,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改当前用户密码（含密码策略验证和审计日志）"""
    from utils.security import verify_password
    
    timer = Timer()
    timer.start()
    
    try:
        # 验证旧密码
        if not verify_password(password_data.old_password, current_user.password_hash):
            # 记录失败
            AuditLogger.log_operation(
                db=db,
                user_id=current_user.id,
                username=current_user.username,
                operation="修改密码失败",
                module="user",
                request=request,
                status="FAILED",
                error_msg="旧密码错误",
                duration=timer.elapsed_ms()
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="旧密码错误"
            )
        
        # 验证新密码强度
        is_valid, error_msg = PasswordPolicy.validate_password_strength(password_data.new_password)
        if not is_valid:
            # 记录失败
            AuditLogger.log_operation(
                db=db,
                user_id=current_user.id,
                username=current_user.username,
                operation="修改密码失败",
                module="user",
                request=request,
                status="FAILED",
                error_msg=f"密码强度不符合要求：{error_msg}",
                duration=timer.elapsed_ms()
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"密码强度不符合要求：{error_msg}"
            )
        
        # 修改密码
        success = crud_user.change_password(db, current_user.id, password_data.new_password)
        if not success:
            raise HTTPException(status_code=500, detail="密码修改失败")
        
        # 更新密码修改时间
        current_user.password_updated_at = datetime.now()
        db.commit()
        
        # 记录成功
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="修改密码",
            module="user",
            request=request,
            status="SUCCESS",
            duration=timer.elapsed_ms()
        )
        
        return {"message": "密码修改成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        # 记录异常
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="修改密码异常",
            module="user",
            request=request,
            status="FAILED",
            error_msg=str(e),
            duration=timer.elapsed_ms()
        )
        raise


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
    request: Request,
    current_user: models.User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """删除用户（仅管理员，含审计日志）"""
    timer = Timer()
    timer.start()
    
    # 不能删除自己
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    try:
        # 获取用户信息
        user = crud_user.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        user_info = {
            "user_id": user.id,
            "username": user.username,
            "name": user.name,
            "role": str(user.role)
        }
        
        # 删除用户
        success = crud_user.delete_user(db, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 记录审计日志
        AuditLogger.log_delete(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="user",
            resource_type="用户",
            resource_id=user_id,
            request=request,
            data=user_info
        )
        
        return {"message": "用户删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="删除用户失败",
            module="user",
            request=request,
            details={"user_id": user_id},
            status="FAILED",
            error_msg=str(e),
            duration=timer.elapsed_ms()
        )
        raise
