"""
经费 CRUD 操作
"""
from sqlalchemy.orm import Session
from typing import Optional, List
import models
import schemas


def get_fund_by_id(db: Session, fund_id: int) -> Optional[models.Fund]:
    """根据ID获取经费记录"""
    return db.query(models.Fund).filter(models.Fund.id == fund_id).first()


def get_funds(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    expense_type: Optional[str] = None,
    return_total: bool = False
):
    """获取经费列表"""
    query = db.query(models.Fund)
    
    if project_id:
        query = query.filter(models.Fund.project_id == project_id)
    if expense_type:
        query = query.filter(models.Fund.expense_type == expense_type)
    
    if return_total:
        total = query.count()
        items = query.order_by(models.Fund.expense_date.desc()).offset(skip).limit(limit).all()
        return total, items
    
    return query.order_by(models.Fund.expense_date.desc()).offset(skip).limit(limit).all()


def create_fund(db: Session, fund: schemas.FundCreate) -> models.Fund:
    """创建经费记录"""
    db_fund = models.Fund(**fund.dict())
    db.add(db_fund)
    db.commit()
    db.refresh(db_fund)
    return db_fund


def update_fund(
    db: Session,
    fund_id: int,
    fund_update: schemas.FundUpdate
) -> Optional[models.Fund]:
    """更新经费记录"""
    db_fund = get_fund_by_id(db, fund_id)
    if not db_fund:
        return None
    
    update_data = fund_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fund, field, value)
    
    db.commit()
    db.refresh(db_fund)
    return db_fund


def delete_fund(db: Session, fund_id: int) -> bool:
    """删除经费记录"""
    db_fund = get_fund_by_id(db, fund_id)
    if not db_fund:
        return False
    
    db.delete(db_fund)
    db.commit()
    return True


def get_project_fund_summary(db: Session, project_id: int) -> dict:
    """获取项目经费汇总"""
    funds = db.query(models.Fund).filter(models.Fund.project_id == project_id).all()
    
    total_expense = sum(fund.amount for fund in funds)
    
    # 按类型统计
    by_type = {}
    for fund in funds:
        expense_type = fund.expense_type
        by_type[expense_type] = by_type.get(expense_type, 0) + fund.amount
    
    return {
        "total_expense": total_expense,
        "by_type": by_type,
        "count": len(funds)
    }


def get_fund_statistics(db: Session) -> dict:
    """经费统计"""
    funds = db.query(models.Fund).all()
    
    total_expense = sum(fund.amount for fund in funds)
    
    # 按类型统计
    by_type = {}
    for fund in funds:
        expense_type = fund.expense_type
        by_type[expense_type] = by_type.get(expense_type, 0) + fund.amount
    
    return {
        "total_expense": total_expense,
        "by_type": by_type
    }
