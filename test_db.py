import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "admission.db")

try:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("✅ Database connected successfully!")
    print(f"📁 DB Path: {DB_PATH}")
    print("")

    # ── Check all tables ──────────────────────────────────
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    tables = cursor.fetchall()
    print("📋 Tables found:")
    if tables:
        for t in tables:
            print(f"   → {t[0]}")
    else:
        print("   ❌ No tables found! Run create_db.py first")
        conn.close()
        exit()

    print("")

    # ── Check row counts ──────────────────────────────────
    cursor.execute("SELECT COUNT(*) FROM roles")
    print(f"👤 Roles:     {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM employee")
    print(f"👨‍💼 Employees: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM course")
    print(f"📚 Courses:   {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM batches")
    print(f"📦 Batches:   {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM students")
    print(f"🎓 Students:  {cursor.fetchone()[0]}")

    print("")

    # ── Check all roles ───────────────────────────────────
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    print("👤 Roles list:")
    for r in roles:
        print(f"   → ID:{r['rl_id']} | {r['rl_name']}")

    print("")

    # ── Check all courses with fees ───────────────────────
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    print("📚 Courses list:")
    for c in courses:
        print(f"   → ID:{c['co_id']} | {c['co_name']} | ₹{c['co_fees']}")

    print("")

    # ── Check all batches ─────────────────────────────────
    cursor.execute("""
        SELECT b.bt_id, b.bt_number, c.co_name,
               b.bt_from_date, b.bt_to_date
        FROM batches b
        JOIN course c ON b.bt_course_id = c.co_id
    """)
    batches = cursor.fetchall()
    print("📦 Batches list:")
    for b in batches:
        print(
            f"   → ID:{b['bt_id']} | "
            f"{b['bt_number']} | "
            f"{b['co_name']} | "
            f"{b['bt_from_date']} to {b['bt_to_date']}"
        )

    print("")

    # ── Check all employees ───────────────────────────────
    cursor.execute("""
        SELECT e.emp_id, e.emp_name, e.emp_username,
               e.emp_comp_id, r.rl_name
        FROM employee e
        JOIN roles r ON e.emp_role = r.rl_id
    """)
    employees = cursor.fetchall()
    print("👨‍💼 Employees list:")
    for e in employees:
        print(
            f"   → ID:{e['emp_id']} | "
            f"{e['emp_name']} | "
            f"@{e['emp_username']} | "
            f"{e['emp_comp_id']} | "
            f"{e['rl_name']}"
        )

    print("")

    # ── Check all students ────────────────────────────────
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print("🎓 Students list:")
    if students:
        for s in students:
            print(
                f"   → ID:{s['st_id']} | "
                f"{s['st_name']} | "
                f"{s['st_mobile']} | "
                f"₹{s['st_fees']}"
            )
    else:
        print("   → No students registered yet")

    print("")

    # ── Test admin login ──────────────────────────────────
    cursor.execute(
        "SELECT * FROM employee "
        "WHERE emp_username=? AND emp_password=?",
        ("admin", "admin123")
    )
    admin = cursor.fetchone()
    if admin:
        print("✅ Admin login works!")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("❌ Admin login failed!")
        print("   Run reset_password.py to fix")

    print("")
    print("✅ All checks completed successfully!")

    conn.close()

except Exception as e:
    print(f"❌ Database error: {e}")
    print("")
    print("💡 Fix options:")
    print("   1. Run: python create_db.py")
    print("   2. Or run: python fix_batches.py")