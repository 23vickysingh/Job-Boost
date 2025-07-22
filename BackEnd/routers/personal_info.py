from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
import os

from .. import models, schemas
from ..database import get_db
from ..auth.dependencies import get_current_user

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/personal-info", tags=["PersonalInfo"])

@router.get("/", response_model=schemas.PersonalInfoOut)
def get_info(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    record = (
        db.query(models.PersonalInformation)
        .filter(models.PersonalInformation.user_id == current_user.id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=404, detail="Personal info not found")
    return record

@router.post("/", response_model=schemas.PersonalInfoOut)
def create_or_update_info(
    info: schemas.PersonalInfoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    record = db.query(models.PersonalInformation).filter(models.PersonalInformation.user_id == current_user.id).first()
    if record:
        for field, value in info.dict(exclude_unset=True).items():
            setattr(record, field, value)
    else:
        record = models.PersonalInformation(user_id=current_user.id, **info.dict())
        db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post("/resume", response_model=schemas.PersonalInfoOut)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in {".pdf", ".doc", ".docx"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    filename = f"{current_user.id}_{uuid4().hex}{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(file.file.read())

    record = db.query(models.PersonalInformation).filter(models.PersonalInformation.user_id == current_user.id).first()
    if not record:
        record = models.PersonalInformation(user_id=current_user.id, resume_path=path)
        db.add(record)
    else:
        record.resume_path = path
    db.commit()
    db.refresh(record)
    return record
