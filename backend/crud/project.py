"""
项目 CRUD 操作
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
import models
import schemas


def get_project_by_id(db: Session, project_id: int) -> Optional[models.Project]:
    """根据ID获取项目"""
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def get_projects(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    pi_id: Optional[int] = None,
    status: Optional[models.ProjectStatus] = None,
    project_type: Optional[str] = None,
    year: Optional[int] = None
) -> List[models.Project]:
    """获取项目列表"""
    query = db.query(models.Project)
    
    if pi_id:
        query = query.filter(models.Project.pi_id == pi_id)
    if status:
        query = query.filter(models.Project.status == status)
    if project_type:
        query = query.filter(models.Project.project_type == project_type)
    if year:
        query = query.filter(db.func.year(models.Project.start_date) == year)
    
    return query.order_by(models.Project.created_at.desc()).offset(skip).limit(limit).all()


def create_project(db: Session, project: schemas.ProjectCreate) -> models.Project:
    """创建项目"""
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(
    db: Session,
    project_id: int,
    project_update: schemas.ProjectUpdate
) -> Optional[models.Project]:
    """更新项目"""
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return None
    
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    """删除项目"""
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        return False
    
    db.delete(db_project)
    db.commit()
    return True


def get_project_statistics(db: Session) -> dict:
    """项目统计"""
    total = db.query(models.Project).count()
    
    # 按状态统计
    status_stats = {}
    for status in models.ProjectStatus:
        count = db.query(models.Project).filter(models.Project.status == status).count()
        status_stats[status.value] = count
    
    return {
        "total": total,
        "by_status": status_stats
    }
