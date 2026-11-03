import sys
from storage import load_tasks, save_tasks


def add_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"✅ Добавлено: {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Список пуст.")
        return
    for i, t in enumerate(tasks, 1):
        mark = "✔" if t["done"] else " "
        print(f"{i}. [{mark}] {t['title']}")


def done_task(index):
    tasks = load_tasks()
    if 0 < index <= len(tasks):
        tasks[index - 1]["done"] = True
        save_tasks(tasks)
        print("Готово!")
    else:
        print("Нет такой задачи.")


def main():
    if len(sys.argv) < 2:
        print("Использование: python todo.py [add|list|done] [аргумент]")
        return

    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_tasks()
    elif cmd == "done" and len(sys.argv) > 2:
        done_task(int(sys.argv[2]))
    else:
        print("Неизвестная команда.")


if __name__ == "__main__":
    main()