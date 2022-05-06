from .models import Item
from sqlmodel import Session, select


def read_item(
        db: Session,
        item_id: int) -> Item | None:
    select_item = select(Item).where(Item.id == item_id)
    return db.exec(select_item).first()


def update_item(
        db: Session,
        item: Item) -> Item:
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
