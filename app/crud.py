from sqlalchemy.orm import Session
from sqlalchemy.sql import extract
from datetime import datetime
from app import models, schemas

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def get_contacts(db: Session, name: str = None, email: str = None):
    query = db.query(models.Contact)
    if name:
        query = query.filter(
            (models.Contact.first_name.ilike(f"%{name}%")) |
            (models.Contact.last_name.ilike(f"%{name}%"))
        )
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))
    return query.all()

def get_contact_by_id(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not db_contact:
        return None
    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id).first()
    if not db_contact:
        return False
    db.delete(db_contact)
    db.commit()
    return True

def get_upcoming_birthdays(db: Session):
    today = datetime.today()
    upcoming_birthdays = db.query(models.Contact).filter(
        extract('month', models.Contact.birthday) == today.month,
        extract('day', models.Contact.birthday) >= today.day
    ).all()
    return upcoming_birthdays