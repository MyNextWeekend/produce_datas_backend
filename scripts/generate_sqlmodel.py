from sqlacodegen.generators import SQLModelGenerator
from sqlalchemy import MetaData, create_engine


def get_table_info():
    engine = create_engine("mysql+pymysql://root:123456@localhost:3306/fms")
    metadata = MetaData()
    generator = SQLModelGenerator(metadata, engine, [])
    metadata.reflect(engine, None, False, None)
    return generator.generate()


def write_file(info: str, file: str):
    with open(file, "w") as f:
        f.write(info)
