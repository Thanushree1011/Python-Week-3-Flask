from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):

    model_config = ConfigDict(extra="forbid")

    supplier_ids: str | None = None
    product_code: str | None = Field(default=None, max_length=25)
    product_name: str | None = Field(default=None, max_length=50)
    description: str | None = None

    standard_cost: Decimal | None = None
    list_price: Decimal = Decimal("0")

    reorder_level: int | None = None
    target_level: int | None = None
    quantity_per_unit: str | None = Field(default=None, max_length=50)

    discontinued: bool = False

    minimum_reorder_quantity: int | None = None
    category: str | None = Field(default=None, max_length=50)


class ProductUpdate(ProductCreate):
    pass