import json
import os

FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
def add_task(title):
    """Добавляет новую задачу и возвращает её."""
    tasks = load_tasks()
    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "title": title,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def list_tasks(show_done=True):
    """Возвращает список задач (по умолчанию — все)."""
    tasks = load_tasks()
    if not show_done:
        tasks = [t for t in tasks if not t["done"]]
    return tasks


def complete_task(task_id):
    """Помечает задачу выполненной. True — если нашлась."""
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            return True
    return False


def delete_task(task_id):
    """Удаляет задачу. True — если нашлась."""
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        return False
    save_tasks(new_tasks)
    return True


def main(argv):
    if len(argv) < 2:
        print("Usage: python tasks.py {add|list|done|del} [args]")
        return 1

    cmd = argv[1]
    if cmd == "add" and len(argv) >= 3:
        task = add_task(" ".join(argv[2:]))
        print(f"Added #{task['id']}: {task['title']}")
    elif cmd == "list":
        for t in list_tasks():
            mark = "✔" if t["done"] else " "
            print(f"[{mark}] #{t['id']} {t['title']}")
    elif cmd == "done" and len(argv) >= 3:
        ok = complete_task(int(argv[2]))
        print("OK" if ok else "Not found")
    elif cmd == "del" and len(argv) >= 3:
        ok = delete_task(int(argv[2]))
        print("Deleted" if ok else "Not found")
    else:
        print("Unknown command")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))