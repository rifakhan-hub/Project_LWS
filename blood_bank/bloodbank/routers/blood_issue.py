from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user, require_roles
from ..models.user import Role, User
from ..schemas.blood_issue import BloodIssueCreate, BloodIssueResponse
from ..services import blood_issue as service
from ..services import staff as staff_service

router = APIRouter(prefix="/blood-issues", tags=["Blood Issues"])


@router.post(
    "/",
    response_model=BloodIssueResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(Role.admin, Role.staff))],
)
def create_blood_issue(
    data: BloodIssueCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    staff_profile = staff_service.get_by_user_id(db, current_user.id)
    if not staff_profile:
        raise HTTPException(
            status_code=400,
            detail="Your account has no linked staff profile, so it cannot issue blood",
        )
    try:
        return service.create(db, data, issued_by_id=staff_profile.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list[BloodIssueResponse],
    dependencies=[Depends(require_roles(Role.admin, Role.staff, Role.doctor))],
)
def list_blood_issues(
    skip: int = 0, limit: int = 100, request_id: int | None = None, db: Session = Depends(get_db)
):
    return service.get_all(db, skip, limit, request_id)


@router.get(
    "/{issue_id}",
    response_model=BloodIssueResponse,
    dependencies=[Depends(require_roles(Role.admin, Role.staff, Role.doctor))],
)
def get_blood_issue(issue_id: int, db: Session = Depends(get_db)):
    issue = service.get_by_id(db, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Blood issue not found")
    return issue