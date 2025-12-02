"""
项目管理路由（符合等保二级要求）
包含完整的审计日志记录
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
import models
import schemas
from crud import project as crud_project
from utils.security import get_current_user
from utils.excel import export_projects_to_excel
from utils.audit import AuditLogger, Timer
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
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """导出项目数据到Excel（含审计日志）"""
    timer = Timer()
    timer.start()
    
    try:
        # 导出数据
        projects = crud_project.get_projects(db, skip=0, limit=10000)
        excel_file = export_projects_to_excel(projects)
        
        # 记录导出操作
        AuditLogger.log_export(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="project",
            resource_type="项目列表",
            request=request,
            details={"total_count": len(projects)}
        )
        
        return StreamingResponse(
            excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=projects.xlsx"}
        )
        
    except Exception as e:
        # 记录失败日志
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="导出项目失败",
            module="project",
            request=request,
            status="FAILED",
            error_msg=str(e),
            duration=timer.elapsed_ms()
        )
        raise


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
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新项目（含审计日志）"""
    timer = Timer()
    timer.start()
    
    try:
        # 创建项目
        new_project = crud_project.create_project(db, project)
        
        # 记录审计日志
        AuditLogger.log_create(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="project",
            resource_type="项目",
            resource_id=new_project.id,
            request=request,
            data={
                "project_name": project.project_name,
                "pi_name": project.pi_name,
                "budget_total": project.budget_total,
                "status": str(project.status)
            }
        )
        
        return new_project
        
    except Exception as e:
        # 记录失败日志
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="创建项目失败",
            module="project",
            request=request,
            status="FAILED",
            error_msg=str(e),
            duration=timer.elapsed_ms()
        )
        raise


@router.put("/{project_id}", response_model=schemas.ProjectResponse, summary="更新项目")
def update_project(
    project_id: int,
    project_update: schemas.ProjectUpdate,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新项目信息（含审计日志和权限检查）"""
    timer = Timer()
    timer.start()
    
    # 检查权限：只有项目负责人或管理员可以修改
    project = crud_project.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    if project.pi_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        # 记录权限拒绝
        AuditLogger.log_permission_denied(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="project",
            request=request,
            reason=f"尝试修改项目ID={project_id}，但无权限"
        )
        raise HTTPException(status_code=403, detail="无权限修改此项目")
    
    try:
        # 收集变更内容
        changes = project_update.model_dump(exclude_unset=True)
        
        # 更新项目
        updated_project = crud_project.update_project(db, project_id, project_update)
        
        # 记录审计日志
        AuditLogger.log_update(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="project",
            resource_type="项目",
            resource_id=project_id,
            request=request,
            changes=changes
        )
        
        return updated_project
        
    except Exception as e:
        # 记录失败日志
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="更新项目失败",
            module="project",
            request=request,
            details={"project_id": project_id},
            status="FAILED",
            error_msg=str(e),
            duration=timer.elapsed_ms()
        )
        raise


@router.delete("/{project_id}", summary="删除项目")
def delete_project(
    project_id: int,
    request: Request,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除项目（含审计日志和权限检查）"""
    timer = Timer()
    timer.start()
    
    # 检查权限
    project = crud_project.get_project_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    if project.pi_id != current_user.id and current_user.role != models.UserRole.ADMIN:
        # 记录权限拒绝
        AuditLogger.log_permission_denied(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="project",
            request=request,
            reason=f"尝试删除项目ID={project_id}，但无权限"
        )
        raise HTTPException(status_code=403, detail="无权限删除此项目")
    
    try:
        # 保存项目信息用于审计
        project_info = {
            "project_id": project.id,
            "project_name": project.project_name,
            "pi_name": project.pi_name
        }
        
        # 删除项目
        success = crud_project.delete_project(db, project_id)
        if not success:
            raise HTTPException(status_code=500, detail="删除失败")
        
        # 记录审计日志
        AuditLogger.log_delete(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            module="project",
            resource_type="项目",
            resource_id=project_id,
            request=request,
            data=project_info
        )
        
        return {"message": "项目删除成功"}
        
    except HTTPException:
        raise
    except Exception as e:
        # 记录失败日志
        AuditLogger.log_operation(
            db=db,
            user_id=current_user.id,
            username=current_user.username,
            operation="删除项目失败",
            module="project",
            request=request,
            details={"project_id": project_id},
            status="FAILED",
            error_msg=str(e),
            duration=timer.elapsed_ms()
        )
        raise
