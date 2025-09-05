from sqlacodegen.generators import SQLModelGenerator
from sqlalchemy import MetaData

from app.core.config import settings
from app.core.dependencies import engine


def get_table_info():
    metadata = MetaData()
    generator = SQLModelGenerator(metadata, engine, [])
    metadata.reflect(engine, None, False, None)
    return generator.generate()


def write_file(info: str):
    file = settings.root_dir.joinpath("app").joinpath("models")
    with open(file.joinpath(f"{settings.db_database}_model.py"), "w") as f:
        f.write(f"# {'=' * 69}\n")
        f.write(f"# {'=' * 10}")
        f.write(" Automatically generate file, do not modify it ! ")
        f.write(f"{'=' * 10}\n")
        f.write(f"# {'=' * 69}\n")
        f.write(info)


if __name__ == '__main__':
    write_file(get_table_info())
