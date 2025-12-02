"""
经费管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
from crud import fund as crud_fund
from utils.security import get_current_user

router = APIRouter()


@router.get("/", response_model=List[schemas.FundResponse], summary="获取经费列表")
def get_funds(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    project_id: Optional[int] = None,
    expense_type: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取经费列表，支持筛选"""
    funds = crud_fund.get_funds(
        db,
        skip=skip,
        limit=limit,
        project_id=project_id,
        expense_type=expense_type
    )
    return funds


@router.get("/project/{project_id}/summary", summary="获取项目经费汇总")
def get_project_fund_summary(
    project_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取指定项目的经费汇总"""
    summary = crud_fund.get_project_fund_summary(db, project_id)
    return summary


@router.get("/{fund_id}", response_model=schemas.FundResponse, summary="获取经费详情")
def get_fund(
    fund_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取经费详细信息"""
    fund = crud_fund.get_fund_by_id(db, fund_id)
    if not fund:
        raise HTTPException(status_code=404, detail="经费记录不存在")
    return fund


@router.post("/", response_model=schemas.FundResponse, summary="创建经费记录")
def create_fund(
    fund: schemas.FundCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新经费记录"""
    return crud_fund.create_fund(db, fund)


@router.put("/{fund_id}", response_model=schemas.FundResponse, summary="更新经费记录")
def update_fund(
    fund_id: int,
    fund_update: schemas.FundUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新经费记录"""
    updated_fund = crud_fund.update_fund(db, fund_id, fund_update)
    if not updated_fund:
        raise HTTPException(status_code=404, detail="经费记录不存在")
    return updated_fund


@router.delete("/{fund_id}", summary="删除经费记录")
def delete_fund(
    fund_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除经费记录"""
    success = crud_fund.delete_fund(db, fund_id)
    if not success:
        raise HTTPException(status_code=404, detail="经费记录不存在")
    
    return {"message": "经费记录删除成功"}
