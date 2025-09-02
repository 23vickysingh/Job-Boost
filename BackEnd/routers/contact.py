from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models, schemas
from database import get_db
from services.email_service import EmailService

router = APIRouter(prefix="/contact", tags=["Contact"])
email_service = EmailService()


@router.post("/submit", response_model=schemas.ContactOut)
async def submit_contact_form(
    contact_data: schemas.ContactCreate,
    db: Session = Depends(get_db),
):
    """Submit a contact form message."""
    try:
        # Validate contact type
        valid_contact_types = ["feedback", "query", "support"]
        if contact_data.contact_type.lower() not in valid_contact_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid contact type. Must be one of: {', '.join(valid_contact_types)}"
            )

        # Create contact entry in database
        db_contact = models.Contact(
            name=contact_data.name.strip(),
            email=contact_data.email,
            subject=contact_data.subject.strip(),
            message=contact_data.message.strip(),
            contact_type=contact_data.contact_type.lower(),
        )
        
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)

        # Send confirmation email to user
        email_sent = email_service.send_contact_confirmation(
            to_email=contact_data.email,
            name=contact_data.name,
            subject=contact_data.subject,
            contact_type=contact_data.contact_type.lower()
        )

        if not email_sent:
            # Log the error but don't fail the entire operation
            print(f"Warning: Failed to send confirmation email to {contact_data.email}")

        return db_contact

    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        print(f"Error submitting contact form: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit contact form")


@router.get("/messages", response_model=List[schemas.ContactOut])
async def get_all_contact_messages(
    limit: int = 50,
    offset: int = 0,
    status: str = None,
    db: Session = Depends(get_db),
):
    """Get all contact messages (admin endpoint)."""
    query = db.query(models.Contact)
    
    if status:
        if status.lower() in ["pending", "resolved"]:
            query = query.filter(models.Contact.status == status.lower())
        else:
            raise HTTPException(status_code=400, detail="Invalid status. Must be 'pending' or 'resolved'")
    
    contacts = query.order_by(models.Contact.created_at.desc()).offset(offset).limit(limit).all()
    return contacts


@router.put("/messages/{contact_id}/resolve")
async def resolve_contact_message(
    contact_id: int,
    db: Session = Depends(get_db),
):
    """Mark a contact message as resolved (admin endpoint)."""
    contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact message not found")
    
    if contact.status == models.ContactStatus.resolved:
        raise HTTPException(status_code=400, detail="Contact message is already resolved")
    
    from datetime import datetime
    contact.status = models.ContactStatus.resolved
    contact.resolved_at = datetime.utcnow()
    
    db.commit()
    db.refresh(contact)
    
    return {"message": "Contact message marked as resolved", "contact_id": contact_id}


@router.get("/stats")
async def get_contact_stats(db: Session = Depends(get_db)):
    """Get contact form statistics (admin endpoint)."""
    total_contacts = db.query(models.Contact).count()
    pending_contacts = db.query(models.Contact).filter(
        models.Contact.status == models.ContactStatus.pending
    ).count()
    resolved_contacts = db.query(models.Contact).filter(
        models.Contact.status == models.ContactStatus.resolved
    ).count()
    
    # Count by contact type
    feedback_count = db.query(models.Contact).filter(
        models.Contact.contact_type == "feedback"
    ).count()
    query_count = db.query(models.Contact).filter(
        models.Contact.contact_type == "query"
    ).count()
    support_count = db.query(models.Contact).filter(
        models.Contact.contact_type == "support"
    ).count()
    
    return {
        "total_contacts": total_contacts,
        "pending_contacts": pending_contacts,
        "resolved_contacts": resolved_contacts,
        "by_type": {
            "feedback": feedback_count,
            "query": query_count,
            "support": support_count
        }
    }
