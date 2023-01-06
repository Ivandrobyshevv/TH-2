from database.engine import engine, Base


def register_models() -> None:
    Base.metadata.create_all(engine)
