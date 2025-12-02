"""
论文 CRUD 操作
"""
from sqlalchemy.orm import Session
from typing import Optional, List
import models
import schemas


def get_paper_by_id(db: Session, paper_id: int) -> Optional[models.Paper]:
    """根据ID获取论文"""
    return db.query(models.Paper).filter(models.Paper.id == paper_id).first()


def get_papers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    creator_id: Optional[int] = None,
    project_id: Optional[int] = None,
    year: Optional[int] = None,
    jcr_zone: Optional[str] = None,
    cas_zone: Optional[str] = None,
    return_total: bool = False
):
    """获取论文列表"""
    query = db.query(models.Paper)
    
    if creator_id:
        query = query.filter(models.Paper.creator_id == creator_id)
    if project_id:
        query = query.filter(models.Paper.project_id == project_id)
    if year:
        query = query.filter(db.func.year(models.Paper.publication_date) == year)
    if jcr_zone:
        query = query.filter(models.Paper.jcr_zone == jcr_zone)
    if cas_zone:
        query = query.filter(models.Paper.cas_zone == cas_zone)
    
    if return_total:
        total = query.count()
        items = query.order_by(models.Paper.publication_date.desc()).offset(skip).limit(limit).all()
        return total, items
    
    return query.order_by(models.Paper.publication_date.desc()).offset(skip).limit(limit).all()


def create_paper(db: Session, paper: schemas.PaperCreate) -> models.Paper:
    """创建论文"""
    db_paper = models.Paper(**paper.dict())
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper


def update_paper(
    db: Session,
    paper_id: int,
    paper_update: schemas.PaperUpdate
) -> Optional[models.Paper]:
    """更新论文"""
    db_paper = get_paper_by_id(db, paper_id)
    if not db_paper:
        return None
    
    update_data = paper_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_paper, field, value)
    
    db.commit()
    db.refresh(db_paper)
    return db_paper


def delete_paper(db: Session, paper_id: int) -> bool:
    """删除论文"""
    db_paper = get_paper_by_id(db, paper_id)
    if not db_paper:
        return False
    
    db.delete(db_paper)
    db.commit()
    return True


def search_papers(db: Session, keyword: str, skip: int = 0, limit: int = 100) -> List[models.Paper]:
    """搜索论文"""
    query = db.query(models.Paper).filter(
        (models.Paper.title.like(f"%{keyword}%")) |
        (models.Paper.authors.like(f"%{keyword}%")) |
        (models.Paper.journal.like(f"%{keyword}%"))
    )
    return query.offset(skip).limit(limit).all()


def get_paper_statistics(db: Session) -> dict:
    """论文统计"""
    total = db.query(models.Paper).count()
    
    # 按年份统计
    year_stats = {}
    papers = db.query(models.Paper).all()
    for paper in papers:
        if paper.publication_date:
            year = paper.publication_date.year
            year_stats[year] = year_stats.get(year, 0) + 1
    
    return {
        "total": total,
        "by_year": year_stats
    }
