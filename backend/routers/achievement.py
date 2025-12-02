"""
成果管理路由（符合等保二级要求）
包含完整的审计日志记录
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
from crud import achievement as crud_achievement
from utils.security import get_current_user
from utils.excel import export_achievements_to_excel
from utils.audit import AuditLogger, Timer
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/", response_model=List[schemas.AchievementResponse], summary="获取成果列表")
def get_achievements(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    achievement_type: Optional[models.AchievementType] = None,
    owner: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取成果列表，支持筛选"""
    achievements = crud_achievement.get_achievements(
        db,
        skip=skip,
        limit=limit,
        achievement_type=achievement_type,
        owner=owner
    )
    return achievements


@router.get("/export", summary="导出成果到Excel")
def export_achievements(
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """导出成果数据到Excel（含审计日志）"""
    try:
        achievements = crud_achievement.get_achievements(db, skip=0, limit=10000)
        excel_file = export_achievements_to_excel(achievements)
        
        AuditLogger.log_export(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="achievement",
            resource_type="成果列表",
            request=request,
            details={"total_count": len(achievements)}
        )
        
        return StreamingResponse(
            excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=achievements.xlsx"}
        )
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="导出成果失败",
            module="achievement",
            request=request,
            status="FAILED",
            error_msg=str(e)
        )
        raise


@router.get("/{achievement_id}", response_model=schemas.AchievementResponse, summary="获取成果详情")
def get_achievement(
    achievement_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取成果详细信息"""
    achievement = crud_achievement.get_achievement_by_id(db, achievement_id)
    if not achievement:
        raise HTTPException(status_code=404, detail="成果不存在")
    return achievement


@router.post("/", response_model=schemas.AchievementResponse, summary="创建成果")
def create_achievement(
    achievement: schemas.AchievementCreate,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新成果记录（含审计日志）"""
    try:
        new_achievement = crud_achievement.create_achievement(db, achievement)
        
        AuditLogger.log_create(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="achievement",
            resource_type="成果",
            resource_id=new_achievement.id,
            request=request,
            data={
                "achievement_type": str(achievement.achievement_type),
                "title": achievement.title,
                "owner": achievement.owner
            }
        )
        
        return new_achievement
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="创建成果失败",
            module="achievement",
            request=request,
            status="FAILED",
            error_msg=str(e)
        )
        raise


@router.put("/{achievement_id}", response_model=schemas.AchievementResponse, summary="更新成果")
def update_achievement(
    achievement_id: int,
    achievement_update: schemas.AchievementUpdate,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新成果信息（含审计日志）"""
    try:
        changes = achievement_update.model_dump(exclude_unset=True)
        updated_achievement = crud_achievement.update_achievement(db, achievement_id, achievement_update)
        
        if not updated_achievement:
            raise HTTPException(status_code=404, detail="成果不存在")
        
        AuditLogger.log_update(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="achievement",
            resource_type="成果",
            resource_id=achievement_id,
            request=request,
            changes=changes
        )
        
        return updated_achievement
    except HTTPException:
        raise
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="更新成果失败",
            module="achievement",
            request=request,
            status="FAILED",
            error_msg=str(e)
        )
        raise


@router.delete("/{achievement_id}", summary="删除成果")
def delete_achievement(
    achievement_id: int,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除成果（含审计日志）"""
    try:
        # 获取成果信息
        achievement = crud_achievement.get_achievement_by_id(db, achievement_id)
        if achievement:
            achievement_info = {
                "achievement_id": achievement.id,
                "title": achievement.title,
                "owner": achievement.owner,
                "achievement_type": str(achievement.achievement_type)
            }
        else:
            achievement_info = {"achievement_id": achievement_id}
        
        success = crud_achievement.delete_achievement(db, achievement_id)
        if not success:
            raise HTTPException(status_code=404, detail="成果不存在")
        
        AuditLogger.log_delete(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="achievement",
            resource_type="成果",
            resource_id=achievement_id,
            request=request,
            data=achievement_info
        )
        
        return {"message": "成果删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="删除成果失败",
            module="achievement",
            request=request,
            status="FAILED",
            error_msg=str(e)
        )
        raise
