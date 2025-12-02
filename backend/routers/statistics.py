"""
统计分析路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models
from utils.security import get_current_user
from crud import project as crud_project
from crud import paper as crud_paper
from crud import fund as crud_fund
from crud import achievement as crud_achievement

router = APIRouter()


@router.get("/overview", summary="系统概览统计")
def get_overview_statistics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取系统整体统计数据
    - 项目总数、论文总数、成果总数
    - 经费总额
    """
    project_count = db.query(models.Project).count()
    paper_count = db.query(models.Paper).count()
    achievement_count = db.query(models.Achievement).count()
    
    # 经费统计
    fund_stats = crud_fund.get_fund_statistics(db)
    
    return {
        "project_count": project_count,
        "paper_count": paper_count,
        "achievement_count": achievement_count,
        "total_expense": fund_stats.get("total_expense", 0),
    }


@router.get("/projects", summary="项目统计")
def get_project_statistics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    项目统计分析
    - 按状态统计
    - 按年份统计
    """
    stats = crud_project.get_project_statistics(db)
    
    # 按年份统计
    projects = db.query(models.Project).all()
    by_year = {}
    for project in projects:
        if project.start_date:
            year = project.start_date.year
            by_year[year] = by_year.get(year, 0) + 1
    
    stats["by_year"] = by_year
    
    return stats


@router.get("/papers", summary="论文统计")
def get_paper_statistics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    论文统计分析
    - 按年份统计
    - 按JCR分区统计
    - 按中科院分区统计
    """
    stats = crud_paper.get_paper_statistics(db)
    
    # 按JCR分区统计
    papers = db.query(models.Paper).all()
    by_jcr = {}
    by_cas = {}
    
    for paper in papers:
        if paper.jcr_zone:
            by_jcr[paper.jcr_zone] = by_jcr.get(paper.jcr_zone, 0) + 1
        if paper.cas_zone:
            by_cas[paper.cas_zone] = by_cas.get(paper.cas_zone, 0) + 1
    
    stats["by_jcr_zone"] = by_jcr
    stats["by_cas_zone"] = by_cas
    
    return stats


@router.get("/funds", summary="经费统计")
def get_fund_statistics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    经费统计分析
    - 总支出
    - 按类型统计
    """
    stats = crud_fund.get_fund_statistics(db)
    return stats


@router.get("/achievements", summary="成果统计")
def get_achievement_statistics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    成果统计分析
    - 总数
    - 按类型统计
    """
    stats = crud_achievement.get_achievement_statistics(db)
    return stats


@router.get("/dashboard", summary="仪表盘数据")
def get_dashboard_data(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取仪表盘所需的综合统计数据
    """
    return {
        "overview": get_overview_statistics(current_user, db),
        "projects": get_project_statistics(current_user, db),
        "papers": get_paper_statistics(current_user, db),
        "funds": get_fund_statistics(current_user, db),
        "achievements": get_achievement_statistics(current_user, db),
    }
