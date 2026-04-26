from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_connection, init_db
from models import (LoginRequest, EmployeeCreate, CourseCreate,
                    BatchCreate, StudentCreate)

app = FastAPI(title="Admission Management System")

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── AUTH ─────────────────────────────────────────────────
@app.post("/login")
def login(req: LoginRequest):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT e.*, r.rl_name FROM employee e "
        "JOIN roles r ON e.emp_role = r.rl_id "
        "WHERE emp_username=? AND emp_password=?",
        (req.username, req.password)
    )
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"success": True, "user": dict(row)}

# ─── ROLES ────────────────────────────────────────────────
@app.get("/roles")
def get_roles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM roles")
    result = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return result

# ─── COURSES ──────────────────────────────────────────────
@app.get("/courses")
def get_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM course")
    result = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return result

@app.post("/courses")
def add_course(course: CourseCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO course (co_name, co_fees) VALUES (?,?)",
        (course.co_name, course.co_fees)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Course added"}

@app.put("/courses/{co_id}")
def update_course(co_id: int, course: CourseCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE course SET co_name=?, co_fees=? WHERE co_id=?",
        (course.co_name, course.co_fees, co_id)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Course updated"}

@app.delete("/courses/{co_id}")
def delete_course(co_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM course WHERE co_id=?", (co_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Course deleted"}

# ─── BATCHES ──────────────────────────────────────────────
@app.get("/batches")
def get_batches():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT b.*, c.co_name, c.co_fees FROM batches b "
        "JOIN course c ON b.bt_course_id = c.co_id"
    )
    result = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return result

@app.get("/batches/by-course/{course_id}")
def get_batches_by_course(course_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM batches WHERE bt_course_id=?", (course_id,)
    )
    result = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return result

@app.post("/batches")
def add_batch(batch: BatchCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO batches (bt_number, bt_course_id, bt_from_date, bt_to_date) "
        "VALUES (?,?,?,?)",
        (batch.bt_number, batch.bt_course_id,
         batch.bt_from_date, batch.bt_to_date)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Batch added"}

@app.put("/batches/{bt_id}")
def update_batch(bt_id: int, batch: BatchCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE batches SET bt_number=?, bt_course_id=?, "
        "bt_from_date=?, bt_to_date=? WHERE bt_id=?",
        (batch.bt_number, batch.bt_course_id,
         batch.bt_from_date, batch.bt_to_date, bt_id)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Batch updated"}

@app.delete("/batches/{bt_id}")
def delete_batch(bt_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM batches WHERE bt_id=?", (bt_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Batch deleted"}

# ─── EMPLOYEES ────────────────────────────────────────────
@app.get("/employees")
def get_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT e.*, r.rl_name FROM employee e "
        "JOIN roles r ON e.emp_role = r.rl_id"
    )
    result = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return result

@app.post("/employees")
def add_employee(emp: EmployeeCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO employee "
        "(emp_name, emp_comp_id, emp_email, emp_mobile, "
        "emp_date_of_join, emp_username, emp_password, emp_role) "
        "VALUES (?,?,?,?,?,?,?,?)",
        (emp.emp_name, emp.emp_comp_id, emp.emp_email,
         emp.emp_mobile, emp.emp_date_of_join,
         emp.emp_username, emp.emp_password, emp.emp_role)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Employee added"}

@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp: EmployeeCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE employee SET emp_name=?, emp_comp_id=?, emp_email=?, "
        "emp_mobile=?, emp_date_of_join=?, emp_username=?, "
        "emp_password=?, emp_role=? WHERE emp_id=?",
        (emp.emp_name, emp.emp_comp_id, emp.emp_email,
         emp.emp_mobile, emp.emp_date_of_join,
         emp.emp_username, emp.emp_password,
         emp.emp_role, emp_id)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Employee updated"}

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employee WHERE emp_id=?", (emp_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Employee deleted"}

# ─── STUDENTS ─────────────────────────────────────────────
@app.get("/students")
def get_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT s.*, b.bt_number, c.co_name, c.co_fees FROM students s "
        "JOIN batches b ON s.st_batch_id = b.bt_id "
        "JOIN course c ON b.bt_course_id = c.co_id"
    )
    result = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return result

@app.post("/students")
def add_student(student: StudentCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT st_id FROM students WHERE st_id=?", (student.st_id,)
    )
    if cursor.fetchone():
        conn.close()
        raise HTTPException(
            status_code=400, detail="Student ID already exists"
        )
    cursor.execute(
        "INSERT INTO students "
        "(st_id, st_name, st_mobile, st_college_name, "
        "st_fees, st_batch_id, st_ref_number) "
        "VALUES (?,?,?,?,?,?,?)",
        (student.st_id, student.st_name, student.st_mobile,
         student.st_college_name, student.st_fees,
         student.st_batch_id, student.st_ref_number)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Student registered"}

@app.put("/students/{st_id}")
def update_student(st_id: str, student: StudentCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE students SET st_name=?, st_mobile=?, "
        "st_college_name=?, st_fees=?, "
        "st_batch_id=?, st_ref_number=? WHERE st_id=?",
        (student.st_name, student.st_mobile,
         student.st_college_name, student.st_fees,
         student.st_batch_id, student.st_ref_number, st_id)
    )
    conn.commit()
    conn.close()
    return {"success": True, "message": "Student updated"}

@app.delete("/students/{st_id}")
def delete_student(st_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE st_id=?", (st_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Student deleted"}