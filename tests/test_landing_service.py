"""Tests for landing page service functionality."""

import pytest
from app.landing import create_contact_inquiry
from app.models import ContactInquiryCreate
from app.database import get_session
from sqlmodel import select


@pytest.fixture
def new_db():
    """Provide a fresh database for each test."""
    from app.database import reset_db

    reset_db()
    yield
    reset_db()


@pytest.fixture
def sample_inquiry_data():
    """Provide sample contact inquiry data for tests."""
    return ContactInquiryCreate(
        name="John Doe",
        email="john.doe@example.com",
        company="Tech Solutions Inc",
        message="Interested in AI solutions for our retail business. Would like to discuss partnership opportunities.",
    )


def test_create_contact_inquiry_success(new_db, sample_inquiry_data):
    """Test successful creation of contact inquiry."""
    inquiry = create_contact_inquiry(sample_inquiry_data)

    assert inquiry is not None
    assert inquiry.id is not None
    assert inquiry.name == "John Doe"
    assert inquiry.email == "john.doe@example.com"
    assert inquiry.company == "Tech Solutions Inc"
    assert (
        inquiry.message
        == "Interested in AI solutions for our retail business. Would like to discuss partnership opportunities."
    )
    assert inquiry.created_at is not None


def test_create_contact_inquiry_stores_in_database(new_db, sample_inquiry_data):
    """Test that contact inquiry is properly stored in database."""
    inquiry = create_contact_inquiry(sample_inquiry_data)
    assert inquiry is not None

    # Verify it's stored in database
    with get_session() as session:
        stored_inquiry = session.get(type(inquiry), inquiry.id)
        assert stored_inquiry is not None
        assert stored_inquiry.name == "John Doe"
        assert stored_inquiry.email == "john.doe@example.com"


def test_create_contact_inquiry_with_long_message(new_db):
    """Test contact inquiry with maximum length message."""
    long_message = "A" * 2000  # Maximum allowed length
    inquiry_data = ContactInquiryCreate(
        name="Jane Smith", email="jane@company.com", company="Big Corp", message=long_message
    )

    inquiry = create_contact_inquiry(inquiry_data)
    assert inquiry is not None
    assert inquiry.message == long_message


def test_create_contact_inquiry_normalizes_email(new_db):
    """Test that email is stored in lowercase."""
    inquiry_data = ContactInquiryCreate(
        name="Test User", email="TEST.USER@EXAMPLE.COM", company="Test Company", message="Test message"
    )

    inquiry = create_contact_inquiry(inquiry_data)
    assert inquiry is not None
    assert inquiry.email == "test.user@example.com"


def test_create_contact_inquiry_with_unicode_characters(new_db):
    """Test contact inquiry with Indonesian characters."""
    inquiry_data = ContactInquiryCreate(
        name="Budi Santoso",
        email="budi@perusahaan.co.id",
        company="PT Teknologi Maju",
        message="Kami tertarik dengan solusi AI untuk meningkatkan efisiensi bisnis kami.",
    )

    inquiry = create_contact_inquiry(inquiry_data)
    assert inquiry is not None
    assert inquiry.name == "Budi Santoso"
    assert inquiry.company == "PT Teknologi Maju"
    assert "efisiensi" in inquiry.message


def test_multiple_inquiries_from_same_email(new_db):
    """Test that multiple inquiries from same email are allowed."""
    inquiry_data_1 = ContactInquiryCreate(
        name="John Doe", email="john@company.com", company="Company A", message="First inquiry"
    )
    inquiry_data_2 = ContactInquiryCreate(
        name="John Doe", email="john@company.com", company="Company B", message="Second inquiry"
    )

    inquiry1 = create_contact_inquiry(inquiry_data_1)
    inquiry2 = create_contact_inquiry(inquiry_data_2)

    assert inquiry1 is not None
    assert inquiry2 is not None
    assert inquiry1.id != inquiry2.id
    assert inquiry1.company == "Company A"
    assert inquiry2.company == "Company B"


def test_inquiry_timestamps_are_different(new_db):
    """Test that inquiries created at different times have different timestamps."""
    import time

    inquiry_data = ContactInquiryCreate(
        name="Test User", email="test@example.com", company="Test Co", message="Test message"
    )

    inquiry1 = create_contact_inquiry(inquiry_data)
    time.sleep(0.001)  # Small delay to ensure different timestamps
    inquiry2 = create_contact_inquiry(inquiry_data)

    assert inquiry1 is not None
    assert inquiry2 is not None
    assert inquiry1.created_at != inquiry2.created_at


def test_create_contact_inquiry_with_minimal_data(new_db):
    """Test contact inquiry with minimal required data."""
    inquiry_data = ContactInquiryCreate(name="A", email="a@b.co", company="X", message="Hi")

    inquiry = create_contact_inquiry(inquiry_data)
    assert inquiry is not None
    assert inquiry.name == "A"
    assert inquiry.email == "a@b.co"
    assert inquiry.company == "X"
    assert inquiry.message == "Hi"


def test_query_all_inquiries(new_db):
    """Test querying all contact inquiries."""
    # Create multiple inquiries
    inquiries_data = [
        ContactInquiryCreate(name="User 1", email="user1@test.com", company="Co 1", message="Msg 1"),
        ContactInquiryCreate(name="User 2", email="user2@test.com", company="Co 2", message="Msg 2"),
        ContactInquiryCreate(name="User 3", email="user3@test.com", company="Co 3", message="Msg 3"),
    ]

    created_inquiries = []
    for data in inquiries_data:
        inquiry = create_contact_inquiry(data)
        assert inquiry is not None
        created_inquiries.append(inquiry)

    # Query all inquiries
    with get_session() as session:
        from app.models import ContactInquiry

        all_inquiries = session.exec(select(ContactInquiry)).all()
        assert len(all_inquiries) == 3

        # Verify all were stored correctly
        names = [inquiry.name for inquiry in all_inquiries]
        assert "User 1" in names
        assert "User 2" in names
        assert "User 3" in names
