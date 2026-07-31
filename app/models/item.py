import uuid

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the item")
    description: str | None = Field(
        None, max_length=500, description="Optional description"
    )
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    in_stock: bool = Field(default=True, description="Whether the item is in stock")


class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float | None = Field(None, gt=0)
    in_stock: bool | None = None


class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True

    class Config:
        from_attributes = True
