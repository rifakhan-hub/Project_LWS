from sqlalchemy.orm import Session

from ..models.blood_request import BloodRequest, RequestStatus


def get_all(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    patient_id: int | None = None,
    status: RequestStatus | None = None,
):
    query = db.query(BloodRequest)
    if patient_id:
        query = query.filter(BloodRequest.patient_id == patient_id)
    if status:
        query = query.filter(BloodRequest.status == status)
    return query.offset(skip).limit(limit).all()


def get_by_id(db: Session, request_id: int):
    return db.query(BloodRequest).filter(BloodRequest.id == request_id).first()


def create(db: Session, data, requested_by_id: int) -> BloodRequest:
    req = BloodRequest(**data.model_dump(), requested_by_id=requested_by_id)
    db.add(req)
    db.commit()
    db.refresh(req)
    return req


def update_status(db: Session, req: BloodRequest, status: RequestStatus) -> BloodRequest:
    req.status = status
    db.commit()
    db.refresh(req)
    return req


def issued_units_count(db: Session, request_id: int) -> int:
    from ..models.blood_issue import BloodIssue
    return db.query(BloodIssue).filter(BloodIssue.request_id == request_id).count()