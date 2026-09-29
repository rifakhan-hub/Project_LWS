from sqlalchemy.orm import Session

from ..models.blood_issue import BloodIssue
from ..models.blood_request import BloodRequest, RequestStatus
from ..models.blood_unit import BloodUnit, UnitStatus
from . import blood_request as request_service


def create(db: Session, data, issued_by_id: int) -> BloodIssue:
    request = db.query(BloodRequest).filter(BloodRequest.id == data.request_id).first()
    if not request:
        raise ValueError("Request not found")
    if request.status != RequestStatus.approved:
        raise ValueError("Request must be approved before it can be fulfilled")

    unit = db.query(BloodUnit).filter(BloodUnit.id == data.blood_unit_id).first()
    if not unit:
        raise ValueError("Blood unit not found")
    if unit.status != UnitStatus.available:
        raise ValueError("Blood unit is not available")
    if unit.blood_group_id != request.blood_group_id or unit.component_id != request.component_id:
        raise ValueError("Blood unit does not match the request's blood group/component")

    # 1. Create the issue record
    issue = BloodIssue(
        request_id=request.id,
        blood_unit_id=unit.id,
        issued_by_id=issued_by_id,
    )
    db.add(issue)

    # 2. The unit leaves available stock
    unit.status = UnitStatus.issued

    db.commit()
    db.refresh(issue)

    # 3. If enough units have now been issued, mark the request fulfilled
    issued_count = request_service.issued_units_count(db, request.id)
    if issued_count >= request.units_requested:
        request_service.update_status(db, request, RequestStatus.fulfilled)

    return issue


def get_all(db: Session, skip: int = 0, limit: int = 100, request_id: int | None = None):
    query = db.query(BloodIssue)
    if request_id:
        query = query.filter(BloodIssue.request_id == request_id)
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, issue_id: int):
    return db.query(BloodIssue).filter(BloodIssue.id == issue_id).first()   