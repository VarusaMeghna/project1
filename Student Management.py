import sqlite3

# Database Connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL
)
""")
conn.commit()


def add_student():
    try:
        name = input("Enter Student Name: ").strip()
        age = int(input("Enter Age: "))
        course = input("Enter Course: ").strip()

        cursor.execute(
            "INSERT INTO students(name, age, course) VALUES (?, ?, ?)",
            (name, age, course)
        )
        conn.commit()
        print("✅ Student Added Successfully!")

    except ValueError:
        print("❌ Age must be a number.")


def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    if not students:
        print("No records found.")
        return

    print("\n----- STUDENTS -----")
    for student in students:
        print(f"ID: {student[0]}")
        print(f"Name: {student[1]}")
        print(f"Age: {student[2]}")
        print(f"Course: {student[3]}")
        print("-" * 20)


def search_student():
    name = input("Enter Student Name: ").strip()

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE ?",
        (f"%{name}%",)
    )

    students = cursor.fetchall()

    if not students:
        print("❌ Student not found.")
        return

    for student in students:
        print(student)


def update_student():
    try:
        student_id = int(input("Enter Student ID: "))

        cursor.execute(
            "SELECT * FROM students WHERE id=?",
            (student_id,)
        )

        student = cursor.fetchone()

        if student is None:
            print("❌ Student not found.")
            return

        name = input("Enter New Name: ").strip()
        age = int(input("Enter New Age: "))
        course = input("Enter New Course: ").strip()

        cursor.execute("""
            UPDATE students
            SET name=?, age=?, course=?
            WHERE id=?
        """, (name, age, course, student_id))

        conn.commit()
        print("✅ Student Updated Successfully!")

    except ValueError:
        print("❌ Invalid input.")


def delete_student():
    try:
        student_id = int(input("Enter Student ID: "))

        cursor.execute(
            "SELECT * FROM students WHERE id=?",
            (student_id,)
        )

        if cursor.fetchone() is None:
            print("❌ Student not found.")
            return

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (student_id,)
        )

        conn.commit()
        print("✅ Student Deleted Successfully!")

    except ValueError:
        print("❌ ID must be a number.")


while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter Choice (1-6): ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        print("Thank You!")
        break

    else:
        print("❌ Invalid Choice. Please enter 1-6.")

conn.close()