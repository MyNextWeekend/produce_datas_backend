from sqlacodegen.generators import SQLModelGenerator
from sqlalchemy import MetaData

from app.config import settings
from app.models import engine


def get_table_info():
    metadata = MetaData()
    generator = SQLModelGenerator(metadata, engine, [])
    metadata.reflect(engine, None, False, None)
    return generator.generate()


def write_file(info: str):
    file = settings.root_dir.joinpath("sqlmodel").joinpath(settings.db_database)
    with open(file, "w") as f:
        f.write(info)


if __name__ == '__main__':
    write_file(get_table_info())
