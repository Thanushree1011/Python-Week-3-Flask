from pydantic import BaseModel, ConfigDict, Field,EmailStr, model_validator
from typing import Optional

class CustomerCreate(BaseModel):

    model_config = ConfigDict(extra="forbid")

    company: str | None = Field(default=None, max_length=50)
    last_name: str | None = Field(default=None, max_length=50)
    first_name: str | None = Field(default=None, max_length=50)
    email_address: EmailStr | None = Field(default=None, max_length=50)
    job_title: str | None = Field(default=None, max_length=50)

    business_phone: str | None = Field(default=None, max_length=25)
    home_phone: str | None = Field(default=None, max_length=25)
    mobile_phone: str | None = Field(default=None, max_length=25)
    fax_number: str | None = Field(default=None, max_length=25)

    address: str | None = None
    city: str | None = Field(default=None, max_length=50)
    state_province: str | None = Field(default=None, max_length=50)
    zip_postal_code: str | None = Field(default=None, max_length=15)
    country_region: str | None = Field(default=None, max_length=50)

    web_page: str | None = None
    notes: str | None = None

    @model_validator(mode="after")
    def not_empty(self):
        if not self.model_fields_set:
            raise ValueError("At least one field is required")
        return self

class CustomerUpdate(CustomerCreate):
    pass