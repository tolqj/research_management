"""
论文管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
from crud import paper as crud_paper
from utils.security import get_current_user
from utils.excel import export_papers_to_excel
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/", response_model=List[schemas.PaperResponse], summary="获取论文列表")
def get_papers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    creator_id: Optional[int] = None,
    project_id: Optional[int] = None,
    year: Optional[int] = None,
    jcr_zone: Optional[str] = None,
    cas_zone: Optional[str] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取论文列表，支持筛选"""
    papers = crud_paper.get_papers(
        db,
        skip=skip,
        limit=limit,
        creator_id=creator_id,
        project_id=project_id,
        year=year,
        jcr_zone=jcr_zone,
        cas_zone=cas_zone
    )
    return papers


@router.get("/search", response_model=List[schemas.PaperResponse], summary="搜索论文")
def search_papers(
    keyword: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """搜索论文（标题、作者、期刊）"""
    papers = crud_paper.search_papers(db, keyword, skip=skip, limit=limit)
    return papers


@router.get("/export", summary="导出论文到Excel")
def export_papers(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """导出论文数据到Excel"""
    papers = crud_paper.get_papers(db, skip=0, limit=10000)
    excel_file = export_papers_to_excel(papers)
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=papers.xlsx"}
    )


@router.get("/{paper_id}", response_model=schemas.PaperResponse, summary="获取论文详情")
def get_paper(
    paper_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取论文详细信息"""
    paper = crud_paper.get_paper_by_id(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    return paper


@router.post("/", response_model=schemas.PaperResponse, summary="创建论文")
def create_paper(
    paper: schemas.PaperCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新论文记录"""
    return crud_paper.create_paper(db, paper)


@router.put("/{paper_id}", response_model=schemas.PaperResponse, summary="更新论文")
def update_paper(
    paper_id: int,
    paper_update: schemas.PaperUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新论文信息"""
    # 检查权限：只有录入人或管理员可以修改
    paper = crud_paper.get_paper_by_id(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    if paper.creator_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="无权限修改此论文")
    
    updated_paper = crud_paper.update_paper(db, paper_id, paper_update)
    return updated_paper


@router.delete("/{paper_id}", summary="删除论文")
def delete_paper(
    paper_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除论文"""
    # 检查权限
    paper = crud_paper.get_paper_by_id(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    if paper.creator_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="无权限删除此论文")
    
    success = crud_paper.delete_paper(db, paper_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除失败")
    
    return {"message": "论文删除成功"}
