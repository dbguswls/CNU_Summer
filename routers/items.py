from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Item
from schemas import ItemCreate, ItemUpdate, ItemResponse

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("", response_model=list[ItemResponse], summary="아이템 목록 조회")
def get_items(
    q: str | None = None,
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    query = db.query(Item)
    if q:
        query = query.filter(Item.name.contains(q))
    if category:
        query = query.filter(Item.category == category)
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    return query.offset(skip).limit(limit).all()


@router.get("/{item_id}", response_model=ItemResponse, summary="특정 아이템 조회")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")
    return item


@router.post("", response_model=ItemResponse, summary="아이템 추가", status_code=201)
def create_item(body: ItemCreate, db: Session = Depends(get_db)):
    item = Item(**body.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ItemResponse, summary="아이템 전체 수정")
def update_item(item_id: int, body: ItemCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")
    for key, value in body.model_dump().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{item_id}", response_model=ItemResponse, summary="아이템 일부 수정")
def patch_item(item_id: int, body: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", summary="아이템 삭제", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")
    db.delete(item)
    db.commit()
