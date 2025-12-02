"""
审计日志工具模块（等保二级要求）
自动记录所有用户操作，用于安全审计和追溯
"""
import time
import json
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import Request
from sqlalchemy.orm import Session
from models import OperationLog


class AuditLogger:
    """审计日志记录器"""
    
    @staticmethod
    def get_client_ip(request: Request) -> str:
        """获取客户端真实IP地址"""
        # 优先从 X-Forwarded-For 获取
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        # 从 X-Real-IP 获取
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # 最后使用客户端地址
        if request.client:
            return request.client.host
        
        return "unknown"
    
    @staticmethod
    def log_operation(
        db: Session,
        user_id: Optional[int],
        username: Optional[str],
        operation: str,
        module: str,
        request: Request,
        details: Optional[Dict[str, Any]] = None,
        status: str = "SUCCESS",
        error_msg: Optional[str] = None,
        duration: Optional[int] = None
    ):
        """
        记录操作日志
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            username: 用户名
            operation: 操作类型（如：登录、创建项目、删除论文等）
            module: 模块名称（如：auth、project、paper等）
            request: FastAPI请求对象
            details: 操作详情（字典格式，会转为JSON）
            status: 操作结果（SUCCESS/FAILED）
            error_msg: 错误信息
            duration: 执行时间（毫秒）
        """
        try:
            log = OperationLog(
                user_id=user_id,
                username=username or "anonymous",
                operation=operation,
                module=module,
                method=request.method,
                path=str(request.url.path),
                details=json.dumps(details, ensure_ascii=False) if details else None,
                ip_address=AuditLogger.get_client_ip(request),
                user_agent=request.headers.get("User-Agent", "")[:500],
                status=status,
                error_msg=error_msg,
                duration=duration
            )
            db.add(log)
            db.commit()
        except Exception as e:
            # 日志记录失败不应影响业务，只打印错误
            print(f"[AuditLog Error] Failed to log operation: {e}")
            db.rollback()
    
    @staticmethod
    def log_login_attempt(
        db: Session,
        username: str,
        request: Request,
        success: bool,
        error_msg: Optional[str] = None
    ):
        """记录登录尝试"""
        AuditLogger.log_operation(
            db=db,
            user_id=None,
            username=username,
            operation="登录" if success else "登录失败",
            module="auth",
            request=request,
            details={"username": username},
            status="SUCCESS" if success else "FAILED",
            error_msg=error_msg
        )
    
    @staticmethod
    def log_logout(
        db: Session,
        user_id: int,
        username: str,
        request: Request
    ):
        """记录登出操作"""
        AuditLogger.log_operation(
            db=db,
            user_id=user_id,
            username=username,
            operation="登出",
            module="auth",
            request=request
        )
    
    @staticmethod
    def log_create(
        db: Session,
        user_id: int,
        username: str,
        module: str,
        resource_type: str,
        resource_id: Any,
        request: Request,
        data: Optional[Dict] = None
    ):
        """记录创建操作"""
        AuditLogger.log_operation(
            db=db,
            user_id=user_id,
            username=username,
            operation=f"创建{resource_type}",
            module=module,
            request=request,
            details={
                "resource_type": resource_type,
                "resource_id": str(resource_id),
                "data": data
            }
        )
    
    @staticmethod
    def log_update(
        db: Session,
        user_id: int,
        username: str,
        module: str,
        resource_type: str,
        resource_id: Any,
        request: Request,
        changes: Optional[Dict] = None
    ):
        """记录更新操作"""
        AuditLogger.log_operation(
            db=db,
            user_id=user_id,
            username=username,
            operation=f"更新{resource_type}",
            module=module,
            request=request,
            details={
                "resource_type": resource_type,
                "resource_id": str(resource_id),
                "changes": changes
            }
        )
    
    @staticmethod
    def log_delete(
        db: Session,
        user_id: int,
        username: str,
        module: str,
        resource_type: str,
        resource_id: Any,
        request: Request
    ):
        """记录删除操作"""
        AuditLogger.log_operation(
            db=db,
            user_id=user_id,
            username=username,
            operation=f"删除{resource_type}",
            module=module,
            request=request,
            details={
                "resource_type": resource_type,
                "resource_id": str(resource_id)
            }
        )
    
    @staticmethod
    def log_query(
        db: Session,
        user_id: int,
        username: str,
        module: str,
        resource_type: str,
        request: Request,
        filters: Optional[Dict] = None
    ):
        """记录查询操作（敏感查询才需要）"""
        AuditLogger.log_operation(
            db=db,
            user_id=user_id,
            username=username,
            operation=f"查询{resource_type}",
            module=module,
            request=request,
            details={
                "resource_type": resource_type,
                "filters": filters
            }
        )
    
    @staticmethod
    def log_export(
        db: Session,
        user_id: int,
        username: str,
        module: str,
        resource_type: str,
        request: Request,
        count: int
    ):
        """记录导出操作"""
        AuditLogger.log_operation(
            db=db,
            user_id=user_id,
            username=username,
            operation=f"导出{resource_type}",
            module=module,
            request=request,
            details={
                "resource_type": resource_type,
                "count": count
            }
        )
    
    @staticmethod
    def log_permission_denied(
        db: Session,
        user_id: Optional[int],
        username: Optional[str],
        module: str,
        request: Request,
        reason: str
    ):
        """记录权限拒绝"""
        AuditLogger.log_operation(
            db=db,
            user_id=user_id,
            username=username or "anonymous",
            operation="权限拒绝",
            module=module,
            request=request,
            details={"reason": reason},
            status="FAILED",
            error_msg=reason
        )


# 时间计时器装饰器（用于统计接口执行时间）
class Timer:
    def __init__(self):
        self.start_time = None
    
    def start(self):
        """开始计时"""
        self.start_time = time.time()
    
    def elapsed_ms(self) -> int:
        """返回经过的毫秒数"""
        if self.start_time is None:
            return 0
        return int((time.time() - self.start_time) * 1000)
