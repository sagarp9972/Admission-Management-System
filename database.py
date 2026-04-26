import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "admission.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS roles (
            rl_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rl_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS employee (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_name TEXT NOT NULL,
            emp_comp_id TEXT UNIQUE NOT NULL,
            emp_email TEXT,
            emp_mobile TEXT,
            emp_date_of_join TEXT,
            emp_username TEXT UNIQUE NOT NULL,
            emp_password TEXT NOT NULL,
            emp_role INTEGER,
            FOREIGN KEY (emp_role) REFERENCES roles(rl_id)
        );

        CREATE TABLE IF NOT EXISTS course (
            co_id INTEGER PRIMARY KEY AUTOINCREMENT,
            co_name TEXT NOT NULL,
            co_fees REAL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS batches (
            bt_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bt_number TEXT NOT NULL,
            bt_course_id INTEGER,
            bt_from_date TEXT,
            bt_to_date TEXT,
            FOREIGN KEY (bt_course_id) REFERENCES course(co_id)
        );

        CREATE TABLE IF NOT EXISTS students (
            st_id TEXT PRIMARY KEY,
            st_name TEXT NOT NULL,
            st_mobile TEXT,
            st_college_name TEXT,
            st_fees REAL DEFAULT 0,
            st_batch_id INTEGER,
            st_ref_number TEXT,
            FOREIGN KEY (st_batch_id) REFERENCES batches(bt_id)
        );
    """)

    cursor.execute("SELECT COUNT(*) FROM roles")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO roles (rl_name)
            VALUES ('Admin'),('Counsellor'),('Accountant')
        """)

    cursor.execute("SELECT COUNT(*) FROM employee")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO employee
            (emp_name, emp_comp_id, emp_email, emp_mobile,
             emp_date_of_join, emp_username, emp_password, emp_role)
            VALUES
            ('Admin User','EMP001','admin@company.com',
             '9999999999','2024-01-01','admin','admin123',1)
        """)

    cursor.execute("SELECT COUNT(*) FROM course")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO course (co_name, co_fees)
            VALUES
            ('Python Full Stack', 15000),
            ('Data Science', 20000),
            ('Web Design', 10000)
        """)

    cursor.execute("SELECT COUNT(*) FROM batches")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO batches (bt_number, bt_course_id, bt_from_date, bt_to_date)
            VALUES
            ('Batch-A', 1, '2024-01-01', '2024-06-01'),
            ('Batch-B', 2, '2024-02-01', '2024-07-01'),
            ('Batch-C', 3, '2024-03-01', '2024-08-01')
        """)

    conn.commit()
    conn.close()
    print("✅ Database ready! (SQLite)")