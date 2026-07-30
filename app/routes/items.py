
from fastapi import APIRouter, HTTPException, status

from app.logger import get_logger
from app.models.item import Item, ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["Items"])
logger = get_logger(__name__)

# In-memory store (replace with a real DB in production)
_store: dict[str, Item] = {}


@router.get("/", response_model=list[Item])
def list_items():
    logger.info("Listing all items, count=%d", len(_store))
    return list(_store.values())


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate):
    item = Item(**payload.model_dump())
    _store[item.id] = item
    logger.info("Created item id=%s name=%s", item.id, item.name)
    return item


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: str):
    item = _store.get(item_id)
    if not item:
        logger.warning("Item not found id=%s", item_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    logger.info("Fetched item id=%s", item_id)
    return item


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: str, payload: ItemUpdate):
    item = _store.get(item_id)
    if not item:
        logger.warning("Update failed — item not found id=%s", item_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    updated_data = payload.model_dump(exclude_unset=True)
    updated_item = item.model_copy(update=updated_data)
    _store[item_id] = updated_item
    logger.info("Updated item id=%s fields=%s", item_id, list(updated_data.keys()))
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str):
    if item_id not in _store:
        logger.warning("Delete failed — item not found id=%s", item_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del _store[item_id]
    logger.info("Deleted item id=%s", item_id)
