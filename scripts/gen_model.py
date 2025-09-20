from sqlacodegen.generators import SQLModelGenerator
from sqlalchemy import MetaData, create_engine

from app.core.config import settings


def get_table_info():
    engine = create_engine(str(settings.mysql.uri), echo=True, pool_size=8, pool_recycle=60 * 30)
    metadata = MetaData()
    generator = SQLModelGenerator(metadata, engine, [], base_class_name="CamelModel")
    metadata.reflect(engine, None, False, None)
    return generator.generate()


def write_file(info: str):
    file = settings.root_dir.joinpath("app").joinpath("models")
    with open(file.joinpath(f"{settings.mysql.database}_model.py"), "w") as f:
        f.write(f"# {'=' * 69}\n")
        f.write(f"# {'=' * 10}")
        f.write(" Automatically generate file, do not modify it ! ")
        f.write(f"{'=' * 10}\n")
        f.write(f"# {'=' * 69}\n")
        f.write("from app.models import CamelModel\n")
        f.write(info.replace(", SQLModel", ""))


if __name__ == '__main__':
    write_file(get_table_info())
