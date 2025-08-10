from nicegui import ui
from app.database import get_session
from app.models import ContactInquiry, ContactInquiryCreate
import logging

logger = logging.getLogger(__name__)


def create_contact_inquiry(data: ContactInquiryCreate) -> ContactInquiry | None:
    """Create a new contact inquiry in the database."""
    try:
        with get_session() as session:
            # Normalize email to lowercase
            inquiry_data = data.model_dump()
            inquiry_data["email"] = inquiry_data["email"].lower()
            inquiry = ContactInquiry(**inquiry_data)
            session.add(inquiry)
            session.commit()
            session.refresh(inquiry)
            return inquiry
    except Exception as e:
        logger.error(f"Failed to create contact inquiry: {e}")
        return None


def create():
    """Create the landing page module."""

    @ui.page("/", title="DV-ONES AI Vision - Solusi AI & Visualisasi Data")
    def landing_page():
        # Apply modern color theme
        ui.colors(
            primary="#2563eb",  # Professional blue
            secondary="#64748b",  # Subtle gray
            accent="#10b981",  # Success green
            positive="#10b981",
            negative="#ef4444",  # Error red
            warning="#f59e0b",  # Warning amber
            info="#3b82f6",  # Info blue
        )

        # Custom CSS for enhanced styling
        ui.add_head_html("""
        <style>
        .hero-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .section-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        .product-card {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .product-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }
        .gradient-button {
            background: linear-gradient(45deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
        }
        .gradient-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
        }
        </style>
        """)

        # Hero Section
        with ui.column().classes("hero-section w-full min-h-screen flex items-center justify-center p-8"):
            with ui.column().classes("max-w-6xl mx-auto text-center"):
                ui.label("Solusi AI & Visualisasi Data yang Mengubah Cara Bisnis Mengambil Keputusan").classes(
                    "text-4xl md:text-6xl font-bold mb-6 leading-tight"
                )
                ui.label(
                    "Kecerdasan buatan dan visualisasi canggih untuk korporasi, edukasi, retail, dan regulasi"
                ).classes("text-xl md:text-2xl mb-8 opacity-90 max-w-4xl mx-auto leading-relaxed")

                # CTA Button
                ui.html(
                    '<a href="#investor-contact" class="gradient-button inline-block px-8 py-4 rounded-lg text-lg font-semibold no-underline">Gabung sebagai Investor</a>'
                )

                # Hero Image Placeholder
                with ui.card().classes("mt-12 p-6 section-card rounded-xl shadow-2xl max-w-4xl mx-auto"):
                    ui.image("hero-ai-dashboard.svg").classes("w-full h-auto rounded-lg")

        # Problem Section
        with ui.column().classes("w-full bg-gray-50 py-16 px-8"):
            with ui.column().classes("max-w-6xl mx-auto"):
                ui.label("Masalah yang Kami Atasi").classes("text-3xl font-bold text-gray-800 text-center mb-12")

                problems = [
                    "Informasi bisnis tidak terstruktur & sulit diakses",
                    "Regulasi & compliance makin kompleks",
                    "Tim non-teknis kesulitan membaca data",
                    "Kebutuhan efisiensi dalam edukasi & pelatihan",
                ]

                with ui.row().classes("gap-6 flex-wrap justify-center"):
                    for problem in problems:
                        with ui.card().classes("p-6 max-w-sm shadow-lg rounded-xl hover:shadow-xl transition-shadow"):
                            ui.icon("error_outline", color="negative").classes("text-4xl mb-4")
                            ui.label(problem).classes("text-gray-700 font-medium leading-relaxed")

        # Solution Section
        with ui.column().classes("w-full bg-white py-16 px-8"):
            with ui.column().classes("max-w-6xl mx-auto"):
                ui.label("Solusi Kami").classes("text-3xl font-bold text-gray-800 text-center mb-8")
                ui.label(
                    "Kami menghadirkan 5 produk AI untuk menyederhanakan analisis, pelaporan, dan pencarian informasi dengan UI ramah pengguna."
                ).classes("text-xl text-gray-600 text-center mb-12 max-w-4xl mx-auto leading-relaxed")

                products = [
                    {"name": "Knowledge-as-a-Service RAG", "icon": "rag.svg"},
                    {"name": "NL2SQL Data Assistant", "icon": "nl2sql.svg"},
                    {"name": "Retail Intelligence Dashboard", "icon": "retail-intel.svg"},
                ]

                with ui.row().classes("gap-8 flex-wrap justify-center"):
                    for product in products:
                        with ui.card().classes("product-card p-8 max-w-sm rounded-xl shadow-lg"):
                            ui.image(product["icon"]).classes("w-16 h-16 mb-6 mx-auto")
                            ui.label(product["name"]).classes("text-xl font-semibold text-gray-800 text-center")

        # Market Section
        with ui.column().classes("w-full bg-gradient-to-br from-blue-50 to-indigo-100 py-16 px-8"):
            with ui.column().classes("max-w-6xl mx-auto"):
                ui.label("Target Pasar").classes("text-3xl font-bold text-gray-800 text-center mb-12")

                markets = [
                    "Perusahaan menengah & besar",
                    "Institusi pendidikan",
                    "eCommerce & retail",
                    "Industri keuangan & kesehatan",
                ]

                with ui.row().classes("gap-6 flex-wrap justify-center"):
                    for market in markets:
                        with ui.card().classes(
                            "p-6 max-w-sm shadow-lg rounded-xl bg-white hover:shadow-xl transition-shadow"
                        ):
                            ui.icon("business", color="primary").classes("text-4xl mb-4")
                            ui.label(market).classes("text-gray-700 font-medium text-center leading-relaxed")

        # Opportunity Section
        with ui.column().classes("w-full bg-white py-16 px-8"):
            with ui.column().classes("max-w-6xl mx-auto"):
                ui.label("Potensi Bisnis").classes("text-3xl font-bold text-gray-800 text-center mb-12")

                opportunities = [
                    "Model SaaS berbasis subscription",
                    "Integrasi multiplatform: Web, WhatsApp, API",
                    "Margin tinggi dari modularisasi produk",
                    "Peluang ekspansi ke Asia Tenggara",
                ]

                with ui.column().classes("max-w-4xl mx-auto space-y-4"):
                    for opportunity in opportunities:
                        with ui.row().classes("items-center p-4 bg-green-50 rounded-lg"):
                            ui.icon("trending_up", color="positive").classes("text-2xl mr-4")
                            ui.label(opportunity).classes("text-gray-700 font-medium text-lg")

        # Investment Section
        with ui.column().classes("w-full bg-gradient-to-r from-purple-600 to-blue-600 py-16 px-8 text-white"):
            with ui.column().classes("max-w-4xl mx-auto text-center"):
                ui.label("Ajakan Investasi").classes("text-3xl font-bold mb-8")
                ui.label(
                    "Kami membuka peluang kolaborasi, pendanaan awal, dan venture partnership untuk mendorong transformasi digital berbasis AI."
                ).classes("text-xl leading-relaxed opacity-90")

        # Contact Section
        with ui.column().classes("w-full bg-gray-50 py-16 px-8").props("id=investor-contact"):
            with ui.column().classes("max-w-4xl mx-auto"):
                ui.label("Tertarik Bergabung?").classes("text-3xl font-bold text-gray-800 text-center mb-6")
                ui.label(
                    "Isi formulir atau hubungi tim kami untuk informasi detail kemitraan dan proposal investasi."
                ).classes("text-xl text-gray-600 text-center mb-12 leading-relaxed")

                # Contact Form
                with ui.card().classes("p-8 shadow-xl rounded-xl bg-white max-w-2xl mx-auto"):
                    with ui.column().classes("gap-6"):
                        name_input = ui.input(label="Nama", placeholder="Masukkan nama lengkap Anda").classes("w-full")
                        email_input = ui.input(label="Email", placeholder="nama@perusahaan.com").classes("w-full")
                        company_input = ui.input(
                            label="Perusahaan", placeholder="Nama perusahaan atau organisasi"
                        ).classes("w-full")
                        message_input = (
                            ui.textarea(
                                label="Pesan",
                                placeholder="Ceritakan minat Anda untuk berkolaborasi atau berinvestasi...",
                            )
                            .classes("w-full")
                            .props("rows=4")
                        )

                        async def submit_contact_form():
                            """Handle contact form submission."""
                            # Validate required fields
                            if not all([name_input.value, email_input.value, company_input.value, message_input.value]):
                                ui.notify("Semua field harus diisi", type="negative")
                                return

                            # Validate email format
                            import re

                            email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                            if not re.match(email_pattern, email_input.value):
                                ui.notify("Format email tidak valid", type="negative")
                                return

                            # Create inquiry
                            inquiry_data = ContactInquiryCreate(
                                name=name_input.value.strip(),
                                email=email_input.value.strip().lower(),
                                company=company_input.value.strip(),
                                message=message_input.value.strip(),
                            )

                            inquiry = create_contact_inquiry(inquiry_data)
                            if inquiry:
                                ui.notify(
                                    "Terima kasih! Pesan Anda telah terkirim. Tim kami akan segera menghubungi Anda.",
                                    type="positive",
                                )
                                # Clear form
                                name_input.value = ""
                                email_input.value = ""
                                company_input.value = ""
                                message_input.value = ""
                            else:
                                ui.notify("Terjadi kesalahan saat mengirim pesan. Silakan coba lagi.", type="negative")

                        ui.button("Kirim Pesan", on_click=submit_contact_form).classes(
                            "gradient-button w-full py-3 text-lg rounded-lg"
                        )

        # Footer
        with ui.column().classes("w-full bg-gray-800 text-white py-12 px-8"):
            with ui.column().classes("max-w-6xl mx-auto text-center"):
                ui.label("DV-ONES AI Vision").classes("text-2xl font-bold mb-4")
                ui.label("© 2024 DV-ONES AI Vision. Transformasi Digital Berbasis Kecerdasan Buatan.").classes(
                    "text-gray-300 text-lg"
                )
