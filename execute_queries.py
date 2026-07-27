from pathlib import Path
import sqlite3
import sys

# Налаштовуємо стандартне виведення на UTF-8 для підтримки кирилиці у Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

BASE_DIR = Path(__file__).parent
DB_NAME = BASE_DIR / "homework.db"


def run_query(query_file_name: str):
    query_file_path = BASE_DIR / query_file_name
    if not query_file_path.exists():
        return

    with open(query_file_path, "r", encoding="utf-8") as f:
        sql = f.read()

    print(f"\n==================== {query_file_name} ====================")
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]

        print(f"Columns: {column_names}")
        for row in results[:10]:
            print(row)
        if len(results) > 10:
            print(f"... and {len(results) - 10} more rows.")


def main():
    for i in range(1, 13):
        query_file = f"query_{i}.sql"
        run_query(query_file)


if __name__ == "__main__":
    main()
