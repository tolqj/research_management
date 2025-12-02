"""
项目管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
from crud import project as crud_project
from utils.security import get_current_user
from utils.excel import export_projects_to_excel
from fastapi.responses import StreamingResponse

router = APIRouter()


@router.get("/", response_model=List[schemas.ProjectResponse], summary="获取项目列表")
def get_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=10000),  # 将最大值从 500 提高到 10000
    pi_id: Optional[int] = None,
    status: Optional[str] = Query(None),
    project_type: Optional[str] = None,
    year: Optional[int] = None,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取项目列表，支持筛选"""
    # 调试日志：打印所有参数
    print(f"[DEBUG] get_projects called with:")
    print(f"  skip={skip}, limit={limit}")
    print(f"  pi_id={pi_id}, status={repr(status)}")
    print(f"  project_type={project_type}, year={year}")
    
    # 处理空字符串的 status，包括 None 和空字符串
    status_enum = None
    if status is not None and status.strip():
        try:
            status_enum = models.ProjectStatus(status)
        except ValueError:
            # 如果无法转换，直接忽略而不是抛异常
            print(f"[DEBUG] Invalid status value: {status}")
            pass
    
    projects = crud_project.get_projects(
        db,
        skip=skip,
        limit=limit,
        pi_id=pi_id,
        status=status_enum,
        project_type=project_type,
        year=year
    )
    return projects


@router.get("/my", response_model=List[schemas.ProjectResponse], summary="获取我的项目")
def get_my_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户负责的项目"""
    projects = crud_project.get_projects(db, skip=skip, limit=limit, pi_id=current_user.id)
    return projects


@router.get("/export", summary="导出项目到Excel")
def export_projects(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """导出项目数据到Excel"""
    projects = crud_project.get_projects(db, skip=0, limit=10000)
    excel_file = export_projects_to_excel(projects)
    
    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=projects.xlsx"}
    )


@router.get("/{project_id}", response_model=schemas.ProjectResponse, summary="获取项目详情")
def get_project(
    project_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取项目详细信息"""
    project = crud_project.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return project


@router.post("/", response_model=schemas.ProjectResponse, summary="创建项目")
def create_project(
    project: schemas.ProjectCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新项目"""
    return crud_project.create_project(db, project)


@router.put("/{project_id}", response_model=schemas.ProjectResponse, summary="更新项目")
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新项目信息"""
    # 检查权限：只有项目负责人或管理员可以修改
    project = crud_project.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    if project.pi_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="无权限修改此项目")
    
    updated_project = crud_project.update_project(db, project_id, project_update)
    return updated_project


@router.delete("/{project_id}", summary="删除项目")
def delete_project(
    project_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除项目"""
    # 检查权限
    project = crud_project.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    if project.pi_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="无权限删除此项目")
    
    success = crud_project.delete_project(db, project_id)
    if not success:
        raise HTTPException(status_code=500, detail="删除失败")
    
    return {"message": "项目删除成功"}
