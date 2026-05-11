from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# DB 없이 메모리(리스트)로 저장
items = [
    {"id": 1, "name": "사과", "price": 1500, "category": "과일"},
    {"id": 2, "name": "바나나", "price": 800, "category": "과일"},
    {"id": 3, "name": "노트북", "price": 1200000, "category": "전자기기"},
    {"id": 4, "name": "마우스", "price": 35000, "category": "전자기기"},
    {"id": 5, "name": "우유", "price": 2500, "category": "유제품"},
]

class Item(BaseModel):
    name: str
    price: int
    category: str = "기타"

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    category: Optional[str] = None


# ──────────────────────────────────────────────
# PATH 파라미터
# URL 경로의 일부 — 특정 리소스를 식별할 때 사용
# 형식: /items/{item_id}
# ──────────────────────────────────────────────

# GET /items/{item_id}
# 예: GET /items/3  →  id가 3인 아이템 반환
@app.get("/items/{item_id}", summary="[Path] 특정 아이템 조회")
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")


# GET /categories/{category}/items/{item_id}
# Path 파라미터 여러 개 사용 예시
# 예: GET /categories/과일/items/1
@app.get("/categories/{category}/items/{item_id}", summary="[Path] 카테고리 + 아이템 조회")
def get_item_by_category(category: str, item_id: int):
    for item in items:
        if item["id"] == item_id and item["category"] == category:
            return item
    raise HTTPException(status_code=404, detail="해당 카테고리에서 아이템을 찾을 수 없음")


# ──────────────────────────────────────────────
# QUERY 파라미터
# URL 뒤에 ?key=value 형태로 붙음 — 필터·정렬·페이징 등 옵션에 사용
# 형식: /items?category=과일&min_price=1000
# ──────────────────────────────────────────────

# GET /items
# 파라미터 없으면 전체, 있으면 조건 필터링
# 예: GET /items?category=과일&min_price=1000&max_price=2000
@app.get("/items", summary="[Query] 아이템 목록 조회 (필터·페이징)")
def get_items(
    category: Optional[str] = None,       # 카테고리 필터
    min_price: Optional[int] = None,       # 최소 가격
    max_price: Optional[int] = None,       # 최대 가격
    skip: int = 0,                         # 페이징: 건너뛸 개수
    limit: int = 10,                       # 페이징: 최대 반환 개수
):
    result = items

    if category:
        result = [i for i in result if i["category"] == category]
    if min_price is not None:
        result = [i for i in result if i["price"] >= min_price]
    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]

    return result[skip : skip + limit]


# GET /search
# 이름 검색 — query 파라미터 q 필수
# 예: GET /search?q=노트
@app.get("/search", summary="[Query] 아이템 이름 검색")
def search_items(q: str):          # q는 기본값 없음 → 필수 query 파라미터
    result = [i for i in items if q in i["name"]]
    return {"query": q, "count": len(result), "results": result}


# ──────────────────────────────────────────────
# PATH + QUERY 혼합
# 특정 리소스(path)에 옵션(query)을 추가하는 패턴
# ──────────────────────────────────────────────

# GET /items/{item_id}/price
# Path로 아이템 지정, Query로 세금 포함 여부 선택
# 예: GET /items/3/price?include_tax=true
@app.get("/items/{item_id}/price", summary="[Path+Query] 아이템 가격 조회 (세금 옵션)")
def get_item_price(item_id: int, include_tax: bool = False):
    for item in items:
        if item["id"] == item_id:
            price = item["price"]
            if include_tax:
                price = int(price * 1.1)   # 부가세 10%
            return {
                "item_id": item_id,
                "name": item["name"],
                "price": price,
                "include_tax": include_tax,
            }
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")


# ──────────────────────────────────────────────
# 기존 CRUD (Path 파라미터 사용)
# ──────────────────────────────────────────────

@app.post("/items", summary="아이템 추가")
def create_item(item: Item):
    new_id = max((i["id"] for i in items), default=0) + 1
    new_item = {"id": new_id, **item.model_dump()}
    items.append(new_item)
    return new_item

@app.put("/items/{item_id}", summary="아이템 전체 수정")
def update_item(item_id: int, item: Item):
    for idx, v in enumerate(items):
        if v["id"] == item_id:
            items[idx] = {"id": item_id, **item.model_dump()}
            return items[idx]
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")

@app.patch("/items/{item_id}", summary="아이템 일부 수정")
def patch_item(item_id: int, item: ItemUpdate):
    for v in items:
        if v["id"] == item_id:
            v.update(item.model_dump(exclude_unset=True))
            return v
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")

@app.delete("/items/{item_id}", summary="아이템 삭제")
def delete_item(item_id: int):
    for idx, v in enumerate(items):
        if v["id"] == item_id:
            items.pop(idx)
            return {"message": "삭제 완료"}
    raise HTTPException(status_code=404, detail="아이템을 찾을 수 없음")
