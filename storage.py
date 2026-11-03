import json
import os
import tempfile

DEFAULT_FILE = "tasks.json"


class StorageError(Exception):
    """Ошибка чтения/записи хранилища задач."""


def load_tasks(path=DEFAULT_FILE):
    """Читает задачи из JSON. Возвращает [] если файла нет.

    Бросает StorageError, если файл повреждён или содержит не список.
    """
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise StorageError(f"Файл {path} повреждён: {e}") from e

    if not isinstance(data, list):
        raise StorageError(
            f"Ожидался список задач в {path}, получено {type(data).__name__}"
        )
    return data


def save_tasks(tasks, path=DEFAULT_FILE):
    """Атомарно сохраняет список задач в JSON.

    Пишет во временный файл в той же директории и делает os.replace —
    это атомарная операция на POSIX и Windows. Так при падении
    процесса старый файл остаётся целым.
    """
    if not isinstance(tasks, list):
        raise StorageError("tasks должен быть списком")

    dir_name = os.path.dirname(os.path.abspath(path))
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix=".tasks-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())  # гарантируем, что данные на диске
        os.replace(tmp_path, path)  # атомарная замена
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise