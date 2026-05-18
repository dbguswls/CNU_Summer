from itertools import count
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/items", tags=["Items"])


class Item(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: int = Field(gt=0)
    category: str = "기타"


class ItemUpdate(BaseModel):
    name: str | None = None
    price: int | None = None
    category: str | None = None


items: list[dict] = [
    {"id": 1, "name": "사과",   "price": 1500,    "category": "과일"},
    {"id": 2, "name": "바나나", "price": 800,     "category": "과일"},
    {"id": 3, "name": "노트북", "price": 1200000, "category": "전자기기"},
    {"id": 4, "name": "마우스", "price": 35000,   "category": "전자기기"},
    {"id": 5, "name": "우유",   "price": 2500,    "category": "유제품"},
]
_id = count(start=6)


@router.get("", summary="아이템 목록 조회")
def get_items(
    q: str | None = None,
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    skip: int = 0,
    limit: int = 10,
):
    result = items
    if q:
        result = [i for i in result if q in i["name"]]
    if category:
        result = [i for i in result if i["category"] == category]
    if min_price is not None:
        result = [i for i in result if i["price"] >= min_price]
    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]
    return result[skip : skip + limit]


@router.get("/{item_id}", summary="특정 아이템 조회")
def get_item(item_id: int, include_tax: bool = False):
    for item in items:
        if item["id"] == item_id:
            result = dict(item)
            if include_tax:
                result["price"] = int(result["price"] * 1.1)
            return result
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")


@router.post("", summary="아이템 추가", status_code=201)
def create_item(item: Item):
    new_item = {"id": next(_id), **item.model_dump()}
    items.append(new_item)
    return new_item


@router.put("/{item_id}", summary="아이템 전체 수정")
def update_item(item_id: int, item: Item):
    for idx, v in enumerate(items):
        if v["id"] == item_id:
            items[idx] = {"id": item_id, **item.model_dump()}
            return items[idx]
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")


@router.patch("/{item_id}", summary="아이템 일부 수정")
def patch_item(item_id: int, item: ItemUpdate):
    for v in items:
        if v["id"] == item_id:
            v.update(item.model_dump(exclude_unset=True))
            return v
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")


@router.delete("/{item_id}", summary="아이템 삭제", status_code=204)
def delete_item(item_id: int):
    for idx, v in enumerate(items):
        if v["id"] == item_id:
            items.pop(idx)
            return
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")
