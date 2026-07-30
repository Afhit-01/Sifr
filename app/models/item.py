from pydantic import BaseModel, Field
from typing import Optional
import uuid


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the item")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    in_stock: bool = Field(default=True, description="Whether the item is in stock")


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    in_stock: Optional[bool] = None


class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

    class Config:
        from_attributes = True
