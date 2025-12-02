"""
成果 CRUD 操作
"""
from sqlalchemy.orm import Session
from typing import Optional, List
import models
import schemas


def get_achievement_by_id(db: Session, achievement_id: int) -> Optional[models.Achievement]:
    """根据ID获取成果"""
    return db.query(models.Achievement).filter(models.Achievement.id == achievement_id).first()


def get_achievements(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    achievement_type: Optional[models.AchievementType] = None,
    owner: Optional[str] = None
) -> List[models.Achievement]:
    """获取成果列表"""
    query = db.query(models.Achievement)
    
    if achievement_type:
        query = query.filter(models.Achievement.achievement_type == achievement_type)
    if owner:
        query = query.filter(models.Achievement.owner.like(f"%{owner}%"))
    
    return query.order_by(models.Achievement.completion_date.desc()).offset(skip).limit(limit).all()


def create_achievement(db: Session, achievement: schemas.AchievementCreate) -> models.Achievement:
    """创建成果"""
    db_achievement = models.Achievement(**achievement.dict())
    db.add(db_achievement)
    db.commit()
    db.refresh(db_achievement)
    return db_achievement


def update_achievement(
    db: Session,
    achievement_id: int,
    achievement_update: schemas.AchievementUpdate
) -> Optional[models.Achievement]:
    """更新成果"""
    db_achievement = get_achievement_by_id(db, achievement_id)
    if not db_achievement:
        return None
    
    update_data = achievement_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_achievement, field, value)
    
    db.commit()
    db.refresh(db_achievement)
    return db_achievement


def delete_achievement(db: Session, achievement_id: int) -> bool:
    """删除成果"""
    db_achievement = get_achievement_by_id(db, achievement_id)
    if not db_achievement:
        return False
    
    db.delete(db_achievement)
    db.commit()
    return True


def get_achievement_statistics(db: Session) -> dict:
    """成果统计"""
    total = db.query(models.Achievement).count()
    
    # 按类型统计
    type_stats = {}
    for achievement_type in models.AchievementType:
        count = db.query(models.Achievement).filter(
            models.Achievement.achievement_type == achievement_type
        ).count()
        type_stats[achievement_type.value] = count
    
    return {
        "total": total,
        "by_type": type_stats
    }
