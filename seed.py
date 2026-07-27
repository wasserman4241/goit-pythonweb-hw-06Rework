from datetime import datetime, timedelta
from pathlib import Path
import random
import sqlite3
from faker import Faker

BASE_DIR = Path(__file__).parent
DB_NAME = BASE_DIR / "homework.db"
SCHEMA_FILE = BASE_DIR / "schema.sql"

fake = Faker("uk_UA")


def init_db():
    """Створення таблиць бази даних за допомогою schema.sql."""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        schema = f.read()

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executescript(schema)
        conn.commit()


def seed_db():
    """Заповнення бази даних випадковими даними за допомогою Faker."""
    groups = ["Група А-1", "Група Б-2", "Група В-3"]
    teachers = [fake.name() for _ in range(4)]
    subjects = [
        "Вища математика",
        "Фізика",
        "Програмування на Python",
        "Бази даних",
        "Веб-розробка",
        "Алгоритми та структури даних"
    ]
    students = [fake.name() for _ in range(40)]

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Очищення перед повторним наповненням
        cursor.execute("DELETE FROM grades;")
        cursor.execute("DELETE FROM students;")
        cursor.execute("DELETE FROM subjects;")
        cursor.execute("DELETE FROM teachers;")
        cursor.execute("DELETE FROM groups;")

        # Reset AUTOINCREMENT counters in sqlite_sequence
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('groups', 'students', 'teachers', 'subjects', 'grades');")

        # 1. Заповнюємо групи
        cursor.executemany("INSERT INTO groups (name) VALUES (?);", [(g,) for g in groups])
        group_ids = [row[0] for row in cursor.execute("SELECT id FROM groups;").fetchall()]

        # 2. Заповнюємо викладачів
        cursor.executemany("INSERT INTO teachers (name) VALUES (?);", [(t,) for t in teachers])
        teacher_ids = [row[0] for row in cursor.execute("SELECT id FROM teachers;").fetchall()]

        # 3. Рівномірно розподіляємо предмети між викладачами
        for i, subj in enumerate(subjects):
            t_id = teacher_ids[i % len(teacher_ids)]
            cursor.execute("INSERT INTO subjects (name, teacher_id) VALUES (?, ?);", (subj, t_id))
        subject_ids = [row[0] for row in cursor.execute("SELECT id FROM subjects;").fetchall()]

        # 4. Заповнюємо студентів (з рівномірною прив'язкою до груп)
        for i, student_name in enumerate(students):
            g_id = group_ids[i % len(group_ids)]
            cursor.execute("INSERT INTO students (name, group_id) VALUES (?, ?);", (student_name, g_id))
        student_ids = [row[0] for row in cursor.execute("SELECT id FROM students;").fetchall()]

        # 5. Заповнюємо оцінки:
        # Враховано зауваження викладача: Гарантуємо кожному студентові хоча б одну оцінку з КОЖНОГО предмета!
        start_date = datetime.now() - timedelta(days=120)
        grades_data = []

        for st_id in student_ids:
            # Крок 5.1: Гарантована оцінка з кожного предмета
            for sub_id in subject_ids:
                grade_val = random.randint(60, 100)
                random_days = random.randint(0, 115)
                grade_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
                grades_data.append((st_id, sub_id, grade_val, grade_date))

            # Крок 5.2: Додаткові випадкові оцінки (до 15-20 оцінок сумарно на студента)
            extra_count = random.randint(9, 14)
            for _ in range(extra_count):
                sub_id = random.choice(subject_ids)
                grade_val = random.randint(60, 100)
                random_days = random.randint(0, 120)
                grade_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
                grades_data.append((st_id, sub_id, grade_val, grade_date))

        cursor.executemany(
            "INSERT INTO grades (student_id, subject_id, grade, date_received) VALUES (?, ?, ?, ?);",
            grades_data
        )

        conn.commit()
    print(f"[+] Database seeded successfully with {len(student_ids)} students and {len(grades_data)} grades.")


def main():
    init_db()
    seed_db()


if __name__ == "__main__":
    main()
