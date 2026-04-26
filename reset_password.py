import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "admission.db")

print("🔐 Admin Password Reset Tool")
print("=" * 40)

# ── Check if database exists ──────────────────────────────
if not os.path.exists(DB_PATH):
    print("❌ Database not found!")
    print("   Run create_db.py first")
    exit()

# ── Show current admin details ────────────────────────────
try:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM employee WHERE emp_id=1"
    )
    current = cursor.fetchone()

    if not current:
        print("❌ No admin found in database!")
        conn.close()
        exit()

    print(f"📋 Current Admin Details:")
    print(f"   ID:       {current['emp_id']}")
    print(f"   Name:     {current['emp_name']}")
    print(f"   Username: {current['emp_username']}")
    print(f"   Password: {current['emp_password']}")
    print("")

    # ── New credentials ───────────────────────────────────
    # ← Change these values to whatever you want
    NEW_NAME     = "Admin User"
    NEW_USERNAME = "admin"
    NEW_PASSWORD = "admin123"

    # ── Update in database ────────────────────────────────
    cursor.execute("""
        UPDATE employee
        SET emp_name=?,
            emp_username=?,
            emp_password=?
        WHERE emp_id=1
    """, (NEW_NAME, NEW_USERNAME, NEW_PASSWORD))

    conn.commit()

    # ── Verify update ─────────────────────────────────────
    cursor.execute(
        "SELECT * FROM employee WHERE emp_id=1"
    )
    updated = cursor.fetchone()

    print("✅ Admin credentials updated!")
    print("")
    print(f"📋 New Admin Details:")
    print(f"   ID:       {updated['emp_id']}")
    print(f"   Name:     {updated['emp_name']}")
    print(f"   Username: {updated['emp_username']}")
    print(f"   Password: {updated['emp_password']}")
    print("")
    print("✅ You can now login with new credentials!")

    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")