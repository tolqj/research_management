"""
审计日志路由（符合等保二级要求）
提供审计日志查询功能，仅管理员和科研秘书可访问
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_, or_
from database import get_db
import models
from utils.security import get_current_user, require_admin, require_secretary

router = APIRouter()


@router.get("/logs", summary="查询审计日志")
def get_audit_logs(
    request: Request,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    username: Optional[str] = Query(None, description="用户名"),
    operation: Optional[str] = Query(None, description="操作类型"),
    module: Optional[str] = Query(None, description="模块名称"),
    status: Optional[str] = Query(None, description="操作结果"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    current_user: models.User = Depends(require_secretary),  # 管理员和科研秘书可查看
    db: Session = Depends(get_db)
):
    """
    查询审计日志
    - 支持多条件筛选
    - 支持分页
    - 管理员和科研秘书可访问
    """
    try:
        # 构建查询条件
        filters = []
        
        if username:
            filters.append(models.OperationLog.username.like(f"%{username}%"))
        
        if operation:
            filters.append(models.OperationLog.operation.like(f"%{operation}%"))
        
        if module:
            filters.append(models.OperationLog.module == module)
        
        if status:
            filters.append(models.OperationLog.status == status)
        
        # 日期范围筛选
        if start_date:
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                filters.append(models.OperationLog.created_at >= start_dt)
            except ValueError:
                raise HTTPException(status_code=400, detail="开始日期格式错误，应为 YYYY-MM-DD")
        
        if end_date:
            try:
                end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
                filters.append(models.OperationLog.created_at < end_dt)
            except ValueError:
                raise HTTPException(status_code=400, detail="结束日期格式错误，应为 YYYY-MM-DD")
        
        # 查询总数
        total = db.query(models.OperationLog).filter(and_(*filters)).count() if filters else db.query(models.OperationLog).count()
        
        # 分页查询
        query = db.query(models.OperationLog)
        if filters:
            query = query.filter(and_(*filters))
        
        logs = query.order_by(desc(models.OperationLog.created_at)).offset((page - 1) * page_size).limit(page_size).all()
        
        # 转换为字典
        result = []
        for log in logs:
            result.append({
                "id": log.id,
                "user_id": log.user_id,
                "username": log.username,
                "operation": log.operation,
                "module": log.module,
                "method": log.method,
                "path": log.path,
                "details": log.details,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
                "status": log.status,
                "error_msg": log.error_msg,
                "duration": log.duration,
                "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else None
            })
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "data": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询审计日志失败: {str(e)}"
        )


@router.get("/logs/statistics", summary="审计日志统计")
def get_audit_statistics(
    days: int = Query(7, ge=1, le=90, description="统计最近N天"),
    current_user: models.User = Depends(require_secretary),
    db: Session = Depends(get_db)
):
    """
    审计日志统计分析
    - 操作类型分布
    - 成功/失败统计
    - 活跃用户统计
    """
    try:
        # 时间范围
        start_date = datetime.now() - timedelta(days=days)
        
        # 操作类型统计
        operation_stats = db.query(
            models.OperationLog.operation,
            func.count(models.OperationLog.id).label('count')
        ).filter(
            models.OperationLog.created_at >= start_date
        ).group_by(
            models.OperationLog.operation
        ).order_by(
            desc('count')
        ).limit(10).all()
        
        # 成功/失败统计
        status_stats = db.query(
            models.OperationLog.status,
            func.count(models.OperationLog.id).label('count')
        ).filter(
            models.OperationLog.created_at >= start_date
        ).group_by(
            models.OperationLog.status
        ).all()
        
        # 活跃用户统计
        user_stats = db.query(
            models.OperationLog.username,
            func.count(models.OperationLog.id).label('count')
        ).filter(
            models.OperationLog.created_at >= start_date
        ).group_by(
            models.OperationLog.username
        ).order_by(
            desc('count')
        ).limit(10).all()
        
        # 每日操作量统计
        daily_stats = db.query(
            func.date(models.OperationLog.created_at).label('date'),
            func.count(models.OperationLog.id).label('count')
        ).filter(
            models.OperationLog.created_at >= start_date
        ).group_by(
            func.date(models.OperationLog.created_at)
        ).order_by(
            'date'
        ).all()
        
        return {
            "operation_stats": [{"operation": op, "count": cnt} for op, cnt in operation_stats],
            "status_stats": [{"status": st or "未知", "count": cnt} for st, cnt in status_stats],
            "user_stats": [{"username": usr, "count": cnt} for usr, cnt in user_stats],
            "daily_stats": [{"date": str(dt), "count": cnt} for dt, cnt in daily_stats]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"统计审计日志失败: {str(e)}"
        )


@router.get("/logs/{log_id}", summary="查询日志详情")
def get_audit_log_detail(
    log_id: int,
    current_user: models.User = Depends(require_secretary),
    db: Session = Depends(get_db)
):
    """查询单条审计日志详情"""
    log = db.query(models.OperationLog).filter(models.OperationLog.id == log_id).first()
    
    if not log:
        raise HTTPException(status_code=404, detail="日志不存在")
    
    return {
        "id": log.id,
        "user_id": log.user_id,
        "username": log.username,
        "operation": log.operation,
        "module": log.module,
        "method": log.method,
        "path": log.path,
        "details": log.details,
        "ip_address": log.ip_address,
        "user_agent": log.user_agent,
        "status": log.status,
        "error_msg": log.error_msg,
        "duration": log.duration,
        "created_at": log.created_at.strftime("%Y-%m-%d %H:%M:%S") if log.created_at else None
    }
