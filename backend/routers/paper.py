"""
论文管理路由（符合等保二级要求）
包含完整的审计日志记录
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
from crud import paper as crud_paper
from utils.security import get_current_user
from utils.excel import export_papers_to_excel
from utils.audit import AuditLogger, Timer
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
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """导出论文数据到Excel（含审计日志）"""
    try:
        papers = crud_paper.get_papers(db, skip=0, limit=10000)
        excel_file = export_papers_to_excel(papers)
        
        AuditLogger.log_export(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="paper",
            resource_type="论文列表",
            request=request,
            details={"total_count": len(papers)}
        )
        
        return StreamingResponse(
            excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=papers.xlsx"}
        )
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="导出论文失败",
            module="paper",
            request=request,
            status="FAILED",
            error_msg=str(e)
        )
        raise


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
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新论文记录（含审计日志）"""
    try:
        new_paper = crud_paper.create_paper(db, paper)
        
        # 记录审计日志
        AuditLogger.log_create(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="paper",
            resource_type="论文",
            resource_id=new_paper.id,
            request=request,
            data={
                "title": paper.title,
                "authors": paper.authors,
                "journal": paper.journal
            }
        )
        
        return new_paper
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="创建论文失败",
            module="paper",
            request=request,
            status="FAILED",
            error_msg=str(e)
        )
        raise


@router.put("/{paper_id}", response_model=schemas.PaperResponse, summary="更新论文")
def update_paper(
    paper_id: int,
    paper_update: schemas.PaperUpdate,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新论文信息（含审计日志和权限检查）"""
    # 检查权限：只有录入人或管理员可以修改
    paper = crud_paper.get_paper_by_id(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    if paper.creator_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        AuditLogger.log_permission_denied(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="paper",
            request=request,
            reason=f"尝试修改论文ID={paper_id}，但无权限"
        )
        raise HTTPException(status_code=403, detail="无权限修改此论文")
    
    try:
        changes = paper_update.model_dump(exclude_unset=True)
        updated_paper = crud_paper.update_paper(db, paper_id, paper_update)
        
        AuditLogger.log_update(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="paper",
            resource_type="论文",
            resource_id=paper_id,
            request=request,
            changes=changes
        )
        
        return updated_paper
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="更新论文失败",
            module="paper",
            request=request,
            status="FAILED",
            error_msg=str(e)
        )
        raise


@router.delete("/{paper_id}", summary="删除论文")
def delete_paper(
    paper_id: int,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除论文（含审计日志和权限检查）"""
    # 检查权限
    paper = crud_paper.get_paper_by_id(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    if paper.creator_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        AuditLogger.log_permission_denied(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="paper",
            request=request,
            reason=f"尝试删除论文ID={paper_id}，但无权限"
        )
        raise HTTPException(status_code=403, detail="无权限删除此论文")
    
    try:
        paper_info = {
            "paper_id": paper.id,
            "title": paper.title,
            "authors": paper.authors
        }
        
        success = crud_paper.delete_paper(db, paper_id)
        if not success:
            raise HTTPException(status_code=500, detail="删除失败")
        
        AuditLogger.log_delete(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="paper",
            resource_type="论文",
            resource_id=paper_id,
            request=request,
            data=paper_info
        )
        
        return {"message": "论文删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="删除论文失败",
            module="paper",
            request=request,
            status="FAILED",
            error_msg=str(e)
        )
        raise
