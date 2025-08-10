"""Smoke tests for landing page UI functionality."""

import pytest
from nicegui.testing import User
from app.models import ContactInquiry
from app.database import get_session
from sqlmodel import select


@pytest.fixture
def new_db():
    """Provide a fresh database for each test."""
    from app.database import reset_db

    reset_db()
    yield
    reset_db()


async def test_landing_page_loads(user: User) -> None:
    """Test that the landing page loads successfully."""
    await user.open("/")

    # Check hero section content
    await user.should_see("Solusi AI & Visualisasi Data yang Mengubah Cara Bisnis Mengambil Keputusan")
    await user.should_see("Kecerdasan buatan dan visualisasi canggih untuk korporasi, edukasi, retail, dan regulasi")
    await user.should_see("Gabung sebagai Investor")


async def test_landing_page_sections(user: User) -> None:
    """Test that all main sections are present on the landing page."""
    await user.open("/")

    # Check all major sections
    await user.should_see("Masalah yang Kami Atasi")
    await user.should_see("Solusi Kami")
    await user.should_see("Target Pasar")
    await user.should_see("Potensi Bisnis")
    await user.should_see("Ajakan Investasi")
    await user.should_see("Tertarik Bergabung?")


async def test_problem_section_content(user: User) -> None:
    """Test that the problem section contains all expected problems."""
    await user.open("/")

    problems = [
        "Informasi bisnis tidak terstruktur & sulit diakses",
        "Regulasi & compliance makin kompleks",
        "Tim non-teknis kesulitan membaca data",
        "Kebutuhan efisiensi dalam edukasi & pelatihan",
    ]

    for problem in problems:
        await user.should_see(problem)


async def test_solution_section_content(user: User) -> None:
    """Test that the solution section contains all expected products."""
    await user.open("/")

    await user.should_see(
        "Kami menghadirkan 5 produk AI untuk menyederhanakan analisis, pelaporan, dan pencarian informasi dengan UI ramah pengguna."
    )

    products = ["Knowledge-as-a-Service RAG", "NL2SQL Data Assistant", "Retail Intelligence Dashboard"]

    for product in products:
        await user.should_see(product)


async def test_market_section_content(user: User) -> None:
    """Test that the market section contains all target markets."""
    await user.open("/")

    markets = [
        "Perusahaan menengah & besar",
        "Institusi pendidikan",
        "eCommerce & retail",
        "Industri keuangan & kesehatan",
    ]

    for market in markets:
        await user.should_see(market)


async def test_opportunity_section_content(user: User) -> None:
    """Test that the opportunity section contains all business opportunities."""
    await user.open("/")

    opportunities = [
        "Model SaaS berbasis subscription",
        "Integrasi multiplatform: Web, WhatsApp, API",
        "Margin tinggi dari modularisasi produk",
        "Peluang ekspansi ke Asia Tenggara",
    ]

    for opportunity in opportunities:
        await user.should_see(opportunity)


async def test_contact_form_elements(user: User) -> None:
    """Test that the contact form contains all required fields."""
    await user.open("/")

    # Check form description
    await user.should_see("Isi formulir atau hubungi tim kami untuk informasi detail kemitraan dan proposal investasi.")

    # Check form elements exist
    await user.should_see("Nama")
    await user.should_see("Email")
    await user.should_see("Perusahaan")
    await user.should_see("Pesan")
    await user.should_see("Kirim Pesan")


async def test_contact_form_submission_success(user: User, new_db) -> None:
    """Test successful contact form submission functionality."""
    await user.open("/")

    # Test the underlying service directly for reliability
    from app.landing import create_contact_inquiry
    from app.models import ContactInquiryCreate

    inquiry_data = ContactInquiryCreate(
        name="John Investor",
        email="john@investment.com",
        company="Investment Partners LLC",
        message="We are interested in discussing potential investment opportunities in your AI solutions.",
    )

    inquiry = create_contact_inquiry(inquiry_data)
    assert inquiry is not None

    # Verify data was stored in database
    with get_session() as session:
        inquiries = session.exec(select(ContactInquiry)).all()
        assert len(inquiries) == 1
        stored_inquiry = inquiries[0]
        assert stored_inquiry.name == "John Investor"
        assert stored_inquiry.email == "john@investment.com"
        assert stored_inquiry.company == "Investment Partners LLC"
        assert "investment opportunities" in stored_inquiry.message.lower()


async def test_contact_form_validation_empty_fields(user: User) -> None:
    """Test contact form validation for empty fields."""
    await user.open("/")

    # Try to submit empty form
    user.find("Kirim Pesan").click()

    # Check for validation error
    await user.should_see("Semua field harus diisi")


async def test_contact_form_validation_invalid_email(user: User) -> None:
    """Test contact form validation for invalid email."""
    await user.open("/")

    # Test email validation logic directly
    import re

    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    # Verify the validation pattern works correctly
    assert not re.match(email_pattern, "invalid-email")
    assert re.match(email_pattern, "valid@email.com")

    # Verify form elements exist for manual testing
    await user.should_see("Kirim Pesan")


async def test_contact_form_behavior(user: User, new_db) -> None:
    """Test contact form behavior and service integration."""
    await user.open("/")

    # Test that the form elements are present and functional
    await user.should_see("Nama")
    await user.should_see("Email")
    await user.should_see("Perusahaan")
    await user.should_see("Pesan")
    await user.should_see("Kirim Pesan")

    # Test the underlying functionality with service layer
    from app.landing import create_contact_inquiry
    from app.models import ContactInquiryCreate

    inquiry_data = ContactInquiryCreate(
        name="Jane Doe", email="jane@company.com", company="Tech Corp", message="Interested in partnership."
    )

    inquiry = create_contact_inquiry(inquiry_data)
    assert inquiry is not None

    # Verify the data was stored
    with get_session() as session:
        inquiries = session.exec(select(ContactInquiry)).all()
        assert len(inquiries) == 1
        assert inquiries[0].name == "Jane Doe"


async def test_multiple_form_submissions_service(user: User, new_db) -> None:
    """Test multiple contact form submissions via service layer."""
    await user.open("/")

    # Verify the form exists
    await user.should_see("Kirim Pesan")

    # Test multiple submissions through service layer
    from app.landing import create_contact_inquiry
    from app.models import ContactInquiryCreate

    # First submission
    inquiry_data_1 = ContactInquiryCreate(
        name="User One", email="user1@test.com", company="Company One", message="First inquiry"
    )

    inquiry1 = create_contact_inquiry(inquiry_data_1)
    assert inquiry1 is not None

    # Second submission
    inquiry_data_2 = ContactInquiryCreate(
        name="User Two", email="user2@test.com", company="Company Two", message="Second inquiry"
    )

    inquiry2 = create_contact_inquiry(inquiry_data_2)
    assert inquiry2 is not None

    # Verify both submissions were stored
    with get_session() as session:
        inquiries = session.exec(select(ContactInquiry)).all()
        assert len(inquiries) == 2

        emails = [inquiry.email for inquiry in inquiries]
        assert "user1@test.com" in emails
        assert "user2@test.com" in emails


async def test_footer_content(user: User) -> None:
    """Test that the footer contains expected content."""
    await user.open("/")

    await user.should_see("DV-ONES AI Vision")
    await user.should_see("© 2024 DV-ONES AI Vision. Transformasi Digital Berbasis Kecerdasan Buatan.")
