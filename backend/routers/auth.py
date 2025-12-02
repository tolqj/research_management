"""
认证路由（符合等保二级要求）
处理用户登录、注册，包含安全策略和审计日志
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database import get_db
import schemas
from crud import user as crud_user
from utils.security import verify_password, create_access_token
from utils.password_policy import PasswordPolicy
from utils.audit import AuditLogger, Timer

router = APIRouter()


@router.post("/register", response_model=schemas.UserResponse, summary="用户注册")
def register(
    user: schemas.UserCreate, 
    request: Request,
    db: Session = Depends(get_db)
):
    """
    用户注册接口（符合等保要求）
    - 检查用户名和邮箱是否已存在
    - 验证密码强度
    - 创建新用户
    - 记录审计日志
    """
    timer = Timer()
    timer.start()
    
    try:
        # 验证密码强度
        is_valid, error_msg = PasswordPolicy.validate_password_strength(user.password)
        if not is_valid:
            # 记录注册失败
            AuditLogger.log_operation(
                db=db,
                user_id=None,
                username=user.username,
                operation="注册失败",
                module="auth",
                request=request,
                details={"username": user.username, "reason": "密码强度不符合要求"},
                status="FAILED",
                error_msg=error_msg,
                duration=timer.elapsed_ms()
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"密码强度不符合要求：{error_msg}"
            )
        
        # 检查用户名是否已存在
        if crud_user.get_user_by_username(db, user.username):
            AuditLogger.log_operation(
                db=db,
                user_id=None,
                username=user.username,
                operation="注册失败",
                module="auth",
                request=request,
                details={"username": user.username, "reason": "用户名已存在"},
                status="FAILED",
                error_msg="用户名已存在",
                duration=timer.elapsed_ms()
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )
        
        # 检查邮箱是否已存在
        if user.email and crud_user.get_user_by_email(db, user.email):
            AuditLogger.log_operation(
                db=db,
                user_id=None,
                username=user.username,
                operation="注册失败",
                module="auth",
                request=request,
                details={"username": user.username, "reason": "邮箱已被使用"},
                status="FAILED",
                error_msg="邮箱已被使用",
                duration=timer.elapsed_ms()
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被使用"
            )
        
        # 创建用户
        db_user = crud_user.create_user(db, user)
        
        # 记录成功注册
        AuditLogger.log_operation(
            db=db,
            user_id=db_user.id,
            username=db_user.username,
            operation="用户注册",
            module="auth",
            request=request,
            details={
                "user_id": db_user.id,
                "username": db_user.username,
                "role": str(db_user.role)
            },
            status="SUCCESS",
            duration=timer.elapsed_ms()
        )
        
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        # 记录异常
        AuditLogger.log_operation(
            db=db,
            user_id=None,
            username=user.username if hasattr(user, 'username') else 'unknown',
            operation="注册异常",
            module="auth",
            request=request,
            details={"error": str(e)},
            status="FAILED",
            error_msg=str(e),
            duration=timer.elapsed_ms()
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="注册失败"
        )


@router.post("/login", response_model=schemas.LoginResponse, summary="用户登录")
def login(
    login_data: schemas.LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    用户登录接口（符合等保二级要求）
    - 验证用户名和密码
    - 检查账号锁定状态
    - 检查密码是否过期
    - 记录登录尝试（成功/失败）
    - 处理登录失败锁定
    - 返回 JWT Token 和用户信息
    """
    timer = Timer()
    timer.start()
    
    # 查找用户
    user = crud_user.get_user_by_username(db, login_data.username)
    
    if not user:
        # 用户不存在，记录失败尝试
        AuditLogger.log_login_attempt(
            db=db,
            username=login_data.username,
            request=request,
            success=False,
            error_msg="用户不存在"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 检查账号是否被锁定
    if PasswordPolicy.is_account_locked(user.locked_until):
        # 计算剩余锁定时间
        remaining_minutes = int((user.locked_until - datetime.now()).total_seconds() / 60) + 1
        error_msg = f"账号已被锁定，请{remaining_minutes}分钟后再试"
        
        AuditLogger.log_login_attempt(
            db=db,
            username=login_data.username,
            request=request,
            success=False,
            error_msg=error_msg
        )
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error_msg
        )
    
    # 验证密码
    if not verify_password(login_data.password, user.password_hash):
        # 密码错误，增加失败次数
        user.login_failures = (user.login_failures or 0) + 1
        
        # 检查是否达到锁定阈值
        if user.login_failures >= PasswordPolicy.MAX_LOGIN_FAILURES:
            user.locked_until = PasswordPolicy.calculate_lockout_time()
            error_msg = f"登录失败次数过多，账号已锁定{PasswordPolicy.LOCKOUT_DURATION_MINUTES}分钟"
        else:
            remaining = PasswordPolicy.MAX_LOGIN_FAILURES - user.login_failures
            error_msg = f"密码错误，还剩{remaining}次尝试机会"
        
        db.commit()
        
        AuditLogger.log_login_attempt(
            db=db,
            username=login_data.username,
            request=request,
            success=False,
            error_msg=error_msg
        )
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg
        )
    
    # 检查密码是否过期
    password_expired = PasswordPolicy.is_password_expired(user.password_updated_at)
    days_until_expiry = PasswordPolicy.days_until_expiry(user.password_updated_at)
    
    # 登录成功，重置失败次数和锁定状态
    user.login_failures = 0
    user.locked_until = None
    user.last_login_at = datetime.now()
    user.last_login_ip = AuditLogger.get_client_ip(request)
    db.commit()
    
    # 记录成功登录
    AuditLogger.log_login_attempt(
        db=db,
        username=login_data.username,
        request=request,
        success=True
    )
    
    # 生成 Token
    access_token = create_access_token(data={"user_id": user.id, "username": user.username})
    
    # 构建响应
    response_data = {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
    
    # 如果密码即将过期或已过期，添加提示
    if password_expired:
        response_data["warning"] = "密码已过期，请尽快修改"
    elif days_until_expiry <= 7:
        response_data["warning"] = f"密码将在 {days_until_expiry} 天后过期，请及时修改"
    
    return response_data
