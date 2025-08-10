from app.database import create_tables
import app.landing


def startup() -> None:
    # this function is called before the first request
    create_tables()
    app.landing.create()
