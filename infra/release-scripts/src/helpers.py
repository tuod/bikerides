from pathlib import Path


def remove_path_prefix(full_path: Path, prefix: Path) -> str:
    """Заменяет абслдютный путь на относительный, если префикс
    prefix является абсолютной частью пути path
    """

    if full_path.is_relative_to(prefix):
        return f"./{full_path.relative_to(prefix)}"
    else:
        return str(full_path)
