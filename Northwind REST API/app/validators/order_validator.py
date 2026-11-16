
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field,model_validator


class OrderCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    employee_id: int | None = None
    customer_id: int = Field(gt=0)

    order_date: datetime | None = None
    shipped_date: datetime | None = None

    shipper_id: int | None = None
    ship_name: str | None = Field(default=None, max_length=50)
    ship_address: str | None = None
    ship_city: str | None = Field(default=None, max_length=50)
    ship_state_province: str | None = Field(default=None, max_length=50)
    ship_zip_postal_code: str | None = Field(default=None, max_length=50)
    ship_country_region: str | None = Field(default=None, max_length=50)

    shipping_fee: Decimal | None = Field(default=None, ge=0)
    taxes: Decimal | None = Field(default=None, ge=0)
    payment_type: str | None = Field(default=None, max_length=50)
    paid_date: datetime | None = None

    notes: str | None = None
    tax_rate: float | None = None
    tax_status_id: int | None = None
    status_id: int | None = None

    @model_validator(mode="after")
    def dates_in_order(self):
        if self.order_date and self.shipped_date and self.shipped_date < self.order_date:
            raise ValueError("shipped_date cannot be before order_date")
        return self


class OrderUpdate(OrderCreate):
    customer_id: int | None = Field(default=None, gt=0)   # optional on update
