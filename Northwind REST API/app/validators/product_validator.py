from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field,model_validator


class ProductCreate(BaseModel):

    model_config = ConfigDict(extra="forbid")

    supplier_ids: str | None = None
    product_code: str | None = Field(default=None, max_length=25)
    product_name: str | None = Field(default=None, max_length=50)
    description: str | None = None

    standard_cost: Decimal | None = Field(default=None,ge=0)
    list_price: Decimal = Field(default=Decimal("0"),ge=0)

    reorder_level: int | None = None
    target_level: int | None = None
    quantity_per_unit: str | None = Field(default=None, max_length=50)

    discontinued: bool = False

    minimum_reorder_quantity: int | None = None
    category: str | None = Field(default=None, max_length=50)

    @model_validator(mode="after")
    def not_empty(self):
        if not self.model_fields_set:
            raise ValueError("At least one field is required")
        return self


class ProductUpdate(ProductCreate):
    pass