from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item import ItemCreate

def create_item(db: Session, item: ItemCreate):
    new_item = Item(name=item.name, value=item.value)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_items(db: Session):
    return db.query(Item).all()