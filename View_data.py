import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "admission.db")

print("=" * 60)
print("   ADMISSION MANAGEMENT SYSTEM - DATA VIEWER")
print("=" * 60)

if not os.path.exists(DB_PATH):
    print("❌ Database not found!")
    print("   Run: python create_db.py")
    exit()

try:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print(f"📁 DB Path: {DB_PATH}")
    print("")

    # ── ROLES TABLE ───────────────────────────────────────
    print("=" * 60)
    print("👤 ROLES TABLE")
    print("=" * 60)
    cursor.execute("SELECT * FROM roles")
    roles = cursor.fetchall()
    if roles:
        print(f"  {'ID':<5} {'Role Name':<20}")
        print("  " + "-" * 25)
        for r in roles:
            print(f"  {r['rl_id']:<5} {r['rl_name']:<20}")
    else:
        print("  No roles found")
    print("")

    # ── EMPLOYEE TABLE ────────────────────────────────────
    print("=" * 60)
    print("👨 EMPLOYEE TABLE")
    print("=" * 60)
    cursor.execute("""
        SELECT e.*, r.rl_name
        FROM employee e
        JOIN roles r ON e.emp_role = r.rl_id
    """)
    employees = cursor.fetchall()
    if employees:
        for emp in employees:
            print(f"  ID:       {emp['emp_id']}")
            print(f"  Name:     {emp['emp_name']}")
            print(f"  Comp ID:  {emp['emp_comp_id']}")
            print(f"  Email:    {emp['emp_email']}")
            print(f"  Mobile:   {emp['emp_mobile']}")
            print(f"  Join:     {emp['emp_date_of_join']}")
            print(f"  Username: {emp['emp_username']}")
            print(f"  Password: {emp['emp_password']}")
            print(f"  Role:     {emp['rl_name']}")
            print("  " + "-" * 30)
    else:
        print("  No employees found")
    print("")

    # ── COURSE TABLE ──────────────────────────────────────
    print("=" * 60)
    print("📚 COURSE TABLE")
    print("=" * 60)
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()
    if courses:
        print(f"  {'ID':<5} {'Course Name':<25} {'Fees':<15}")
        print("  " + "-" * 45)
        for c in courses:
            print(f"  {c['co_id']:<5} {c['co_name']:<25} Rs.{c['co_fees']:<15}")
    else:
        print("  No courses found")
    print("")

    # ── BATCHES TABLE ─────────────────────────────────────
    print("=" * 60)
    print("📦 BATCHES TABLE")
    print("=" * 60)
    cursor.execute("""
        SELECT b.*, c.co_name
        FROM batches b
        JOIN course c ON b.bt_course_id = c.co_id
    """)
    batches = cursor.fetchall()
    if batches:
        print(f"  {'ID':<5} {'Batch':<12} {'Course':<22} {'From':<12} {'To':<12}")
        print("  " + "-" * 65)
        for b in batches:
            print(
                f"  {b['bt_id']:<5} "
                f"{b['bt_number']:<12} "
                f"{b['co_name']:<22} "
                f"{b['bt_from_date']:<12} "
                f"{b['bt_to_date']:<12}"
            )
    else:
        print("  No batches found")
    print("")

    # ── STUDENTS TABLE ────────────────────────────────────
    print("=" * 60)
    print("🎓 STUDENTS TABLE")
    print("=" * 60)
    cursor.execute("""
        SELECT s.*, b.bt_number, c.co_name
        FROM students s
        JOIN batches b ON s.st_batch_id = b.bt_id
        JOIN course c ON b.bt_course_id = c.co_id
    """)
    students = cursor.fetchall()
    if students:
        print(f"  Total Students: {len(students)}")
        print("")
        for s in students:
            print(f"  ID:      {s['st_id']}")
            print(f"  Name:    {s['st_name']}")
            print(f"  Mobile:  {s['st_mobile']}")
            print(f"  College: {s['st_college_name']}")
            print(f"  Fees:    Rs.{s['st_fees']}")
            print(f"  Batch:   {s['bt_number']}")
            print(f"  Course:  {s['co_name']}")
            print(f"  Ref No:  {s['st_ref_number']}")
            print("  " + "-" * 30)
    else:
        print("  No students registered yet")
    print("")

    # ── SUMMARY ───────────────────────────────────────────
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    cursor.execute("SELECT COUNT(*) FROM roles")
    print(f"  Roles:     {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM employee")
    print(f"  Employees: {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM course")
    print(f"  Courses:   {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM batches")
    print(f"  Batches:   {cursor.fetchone()[0]}")
    cursor.execute("SELECT COUNT(*) FROM students")
    print(f"  Students:  {cursor.fetchone()[0]}")
    cursor.execute("SELECT SUM(st_fees) FROM students")
    total = cursor.fetchone()[0]
    print(f"  Total Fees Collected: Rs.{total or 0}")
    print("")
    print("✅ Done!")
    print("=" * 60)

    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")
    print("   Run: python create_db.py")