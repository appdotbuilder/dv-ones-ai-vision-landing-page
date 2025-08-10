from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class ContactInquiry(SQLModel, table=True):
    """Model for storing contact inquiries from potential investors and partners."""

    __tablename__ = "contact_inquiries"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, description="Name of the person making the inquiry")
    email: str = Field(
        max_length=255, regex=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Email address"
    )
    company: str = Field(max_length=200, description="Company or organization name")
    message: str = Field(max_length=2000, description="Inquiry message or details")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when inquiry was submitted")


class ContactInquiryCreate(SQLModel, table=False):
    """Schema for creating a new contact inquiry."""

    name: str = Field(max_length=100)
    email: str = Field(max_length=255)
    company: str = Field(max_length=200)
    message: str = Field(max_length=2000)


class ContactInquiryRead(SQLModel, table=False):
    """Schema for reading contact inquiry data."""

    id: int
    name: str
    email: str
    company: str
    message: str
    created_at: datetime
