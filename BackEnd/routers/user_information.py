from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/information", tags=["UserInformation"])


@router.get("/", response_model=schemas.UserInformationOut)
def get_information(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    record = (
        db.query(models.UserInformation)
        .filter(models.UserInformation.user_id == current_user.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Information not found")
    return record


@router.post("/", response_model=schemas.UserInformationOut)
def create_or_update_information(
    info: schemas.UserInformationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    record = (
        db.query(models.UserInformation)
        .filter(models.UserInformation.user_id == current_user.id)
        .first()
    )
    if record:
        for field, value in info.dict(exclude_unset=True).items():
            setattr(record, field, value)
    else:
        record = models.UserInformation(user_id=current_user.id, **info.dict())
        db.add(record)
    db.commit()
    db.refresh(record)
    return record
