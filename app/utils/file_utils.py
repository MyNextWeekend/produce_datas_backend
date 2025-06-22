from pathlib import Path
from typing import List


def get_file_by_pattern(input_path: Path, pattern: str = "*") -> List[Path]:
    """
    获取符合指定模式的文件列表。
    :param input_path:输入路径，可以是文件或目录。
    :param pattern:匹配的文件模式，默认为 "*"。
    :return:符合模式的文件路径列表。
    """
    if not input_path.exists():
        raise FileNotFoundError(f"输入的路径不存在: {input_path}")

    # 如果是文件，直接判断是否匹配模式
    if input_path.is_file():
        return [input_path] if input_path.match(pattern) else []

    # 如果是目录，递归查找符合模式的文件
    return [item for item in input_path.rglob(pattern) if item.is_file()]
