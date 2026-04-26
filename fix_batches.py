import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "admission.db")

print("🔧 Fix Batches Tool")
print("=" * 40)

# ── Check if database exists ──────────────────────────────
if not os.path.exists(DB_PATH):
    print("❌ Database not found!")
    print("   Run create_db.py first")
    exit()

try:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # ── Show current batches ──────────────────────────────
    cursor.execute("""
        SELECT b.*, c.co_name, c.co_fees
        FROM batches b
        JOIN course c ON b.bt_course_id = c.co_id
    """)
    rows = cursor.fetchall()

    print(f"📦 Current batches ({len(rows)} found):")
    for r in rows:
        print(
            f"   → ID:{r['bt_id']} | "
            f"{r['bt_number']} | "
            f"{r['co_name']} | "
            f"{r['bt_from_date']} to {r['bt_to_date']}"
        )

    print("")

    # ── Check courses exist ───────────────────────────────
    cursor.execute("SELECT * FROM course")
    courses = cursor.fetchall()

    if not courses:
        print("❌ No courses found!")
        print("   Adding default courses first...")
        cursor.execute(
            "INSERT INTO course (co_name, co_fees) "
            "VALUES ('Python Full Stack', 15000)"
        )
        cursor.execute(
            "INSERT INTO course (co_name, co_fees) "
            "VALUES ('Data Science', 20000)"
        )
        cursor.execute(
            "INSERT INTO course (co_name, co_fees) "
            "VALUES ('Web Design', 10000)"
        )
        conn.commit()
        print("✅ Default courses added!")
        print("")

    # ── Delete all existing batches ───────────────────────
    cursor.execute("DELETE FROM batches")
    conn.commit()
    print("🗑️  All old batches deleted")

    # ── Re-insert clean batch data ────────────────────────
    cursor.execute("""
        INSERT INTO batches
        (bt_number, bt_course_id, bt_from_date, bt_to_date)
        VALUES ('Batch-A', 1, '2024-01-01', '2024-06-01')
    """)
    cursor.execute("""
        INSERT INTO batches
        (bt_number, bt_course_id, bt_from_date, bt_to_date)
        VALUES ('Batch-B', 2, '2024-02-01', '2024-07-01')
    """)
    cursor.execute("""
        INSERT INTO batches
        (bt_number, bt_course_id, bt_from_date, bt_to_date)
        VALUES ('Batch-C', 3, '2024-03-01', '2024-08-01')
    """)
    conn.commit()

    # ── Show updated batches ──────────────────────────────
    cursor.execute("""
        SELECT b.*, c.co_name, c.co_fees
        FROM batches b
        JOIN course c ON b.bt_course_id = c.co_id
    """)
    updated = cursor.fetchall()

    print("")
    print(f"✅ Batches fixed! ({len(updated)} batches now):")
    for r in updated:
        print(
            f"   → ID:{r['bt_id']} | "
            f"{r['bt_number']} | "
            f"{r['co_name']} | "
            f"₹{r['co_fees']} | "
            f"{r['bt_from_date']} to {r['bt_to_date']}"
        )

    print("")
    print("✅ Done! Batches are clean now.")

    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")
    print("")
    print("💡 Fix: Run create_db.py to recreate the database")
    print("   python create_db.py")