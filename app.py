import streamlit as st
import requests

API      = "http://127.0.0.1:8000"
UPI_ID   = "your-upi-id@upi"
UPI_NAME = "Admission System"

st.set_page_config(page_title="Admission System", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in   = False
    st.session_state.user        = None
if "edit_student" not in st.session_state:
    st.session_state.edit_student  = None
if "edit_employee" not in st.session_state:
    st.session_state.edit_employee = None
if "edit_course" not in st.session_state:
    st.session_state.edit_course   = None
if "edit_batch" not in st.session_state:
    st.session_state.edit_batch    = None

# ─── LOGIN ────────────────────────────────────────────────
def login_page():
    st.title("🎓 Admission Management System")
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        res = requests.post(f"{API}/login", json={
            "username": username, "password": password
        })
        if res.status_code == 200:
            st.session_state.logged_in = True
            st.session_state.user = res.json()["user"]
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# ─── UPI PAYMENT ──────────────────────────────────────────
def show_payment(fees, student_name):
    st.markdown("---")
    st.subheader("💳 Pay Fees")
    upi_url = (
        f"upi://pay?pa={UPI_ID}&pn={UPI_NAME}"
        f"&am={fees}&cu=INR&tn=Fees for {student_name}"
    )
    qr_api = (
        f"https://api.qrserver.com/v1/create-qr-code/"
        f"?size=200x200&data={upi_url}"
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📱 Scan QR Code")
        st.image(qr_api, width=200)
        st.caption(f"Amount: ₹{fees}")
        st.caption(f"UPI ID: {UPI_ID}")
    with col2:
        st.markdown("### 💸 Or Pay via UPI ID")
        st.code(UPI_ID)
        st.markdown(f"**Amount:** ₹{fees}")
        st.info(
            "1. Open GPay / PhonePe / Paytm\n"
            "2. Scan QR or enter UPI ID\n"
            "3. Enter amount and pay\n"
            "4. Save transaction reference number"
        )

# ─── DASHBOARD ────────────────────────────────────────────
def admin_dashboard():
    user = st.session_state.user
    st.sidebar.title(f"👋 {user['emp_name']}")
    st.sidebar.write(f"Role: **{user['rl_name']}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    menu = st.sidebar.radio("Menu", [
        "📊 Dashboard",
        "👨‍💼 Add Employee",
        "👥 View Employees",
        "📚 Add Course",
        "📚 Manage Courses",
        "📦 Add Batch",
        "📦 Manage Batches",
        "🎓 Register Student",
        "📋 View Students",
    ])

    # ── DASHBOARD ─────────────────────────────────────────
    if menu == "📊 Dashboard":
        st.title("Dashboard")
        col1, col2, col3 = st.columns(3)
        students = requests.get(f"{API}/students").json()
        courses  = requests.get(f"{API}/courses").json()
        batches  = requests.get(f"{API}/batches").json()
        col1.metric("Total Students", len(students))
        col2.metric("Total Courses",  len(courses))
        col3.metric("Total Batches",  len(batches))

    # ── ADD EMPLOYEE ──────────────────────────────────────
    elif menu == "👨‍💼 Add Employee":
        st.title("Add Employee")
        roles    = requests.get(f"{API}/roles").json()
        role_map = {r["rl_name"]: r["rl_id"] for r in roles}
        with st.form("emp_form"):
            col1, col2 = st.columns(2)
            with col1:
                emp_name    = st.text_input("Employee Name")
                emp_comp_id = st.text_input("Company ID")
                emp_email   = st.text_input("Email ID")
                emp_mobile  = st.text_input("Mobile Number")
            with col2:
                emp_doj      = st.date_input("Date of Join")
                emp_role     = st.selectbox("Role", list(role_map.keys()))
                emp_username = st.text_input("Username")
                emp_password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Add Employee")
        if submit:
            res = requests.post(f"{API}/employees", json={
                "emp_name":         emp_name,
                "emp_comp_id":      emp_comp_id,
                "emp_email":        emp_email,
                "emp_mobile":       emp_mobile,
                "emp_date_of_join": str(emp_doj),
                "emp_username":     emp_username,
                "emp_password":     emp_password,
                "emp_role":         role_map[emp_role]
            })
            if res.status_code == 200:
                st.success("✅ Employee added!")
            else:
                st.error(f"❌ Failed: {res.text}")

    # ── VIEW EMPLOYEES ────────────────────────────────────
    elif menu == "👥 View Employees":
        st.title("Employee List")
        if st.session_state.edit_employee:
            emp = st.session_state.edit_employee
            st.subheader(f"✏️ Edit Employee — {emp['emp_name']}")
            roles      = requests.get(f"{API}/roles").json()
            role_map   = {r["rl_name"]: r["rl_id"] for r in roles}
            role_names = list(role_map.keys())
            cur_role   = next(
                (r["rl_name"] for r in roles
                 if r["rl_id"] == emp["emp_role"]), role_names[0]
            )
            with st.form("edit_emp_form"):
                col1, col2 = st.columns(2)
                with col1:
                    e_name    = st.text_input("Employee Name",  emp["emp_name"])
                    e_comp_id = st.text_input("Company ID",     emp["emp_comp_id"])
                    e_email   = st.text_input("Email ID",       emp.get("emp_email", ""))
                    e_mobile  = st.text_input("Mobile Number",  emp.get("emp_mobile", ""))
                with col2:
                    e_doj      = st.text_input("Date of Join",  emp.get("emp_date_of_join", ""))
                    e_role     = st.selectbox("Role", role_names,
                                    index=role_names.index(cur_role))
                    e_username = st.text_input("Username",      emp["emp_username"])
                    e_password = st.text_input("Password",      emp["emp_password"])
                col_s, col_c = st.columns(2)
                save   = col_s.form_submit_button("💾 Save Changes")
                cancel = col_c.form_submit_button("❌ Cancel")
            if save:
                res = requests.put(
                    f"{API}/employees/{emp['emp_id']}", json={
                        "emp_name":         e_name,
                        "emp_comp_id":      e_comp_id,
                        "emp_email":        e_email,
                        "emp_mobile":       e_mobile,
                        "emp_date_of_join": e_doj,
                        "emp_username":     e_username,
                        "emp_password":     e_password,
                        "emp_role":         role_map[e_role]
                    }
                )
                if res.status_code == 200:
                    st.success("✅ Employee updated!")
                    st.session_state.edit_employee = None
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {res.text}")
            if cancel:
                st.session_state.edit_employee = None
                st.rerun()
        else:
            employees = requests.get(f"{API}/employees").json()
            if employees:
                cols = st.columns([1, 2, 2, 2, 2, 2, 2, 1, 1])
                for col, h in zip(cols, [
                    "ID", "Name", "Comp ID", "Email",
                    "Mobile", "Join Date", "Role", "Edit", "Del"
                ]):
                    col.markdown(f"**{h}**")
                st.markdown("---")
                for emp in employees:
                    cols = st.columns([1, 2, 2, 2, 2, 2, 2, 1, 1])
                    cols[0].write(emp["emp_id"])
                    cols[1].write(emp["emp_name"])
                    cols[2].write(emp["emp_comp_id"])
                    cols[3].write(emp.get("emp_email", ""))
                    cols[4].write(emp.get("emp_mobile", ""))
                    cols[5].write(emp.get("emp_date_of_join", ""))
                    cols[6].write(emp["rl_name"])
                    if cols[7].button("✏️", key=f"edit_emp_{emp['emp_id']}"):
                        st.session_state.edit_employee = emp
                        st.rerun()
                    if cols[8].button("🗑️", key=f"del_emp_{emp['emp_id']}"):
                        requests.delete(f"{API}/employees/{emp['emp_id']}")
                        st.success(f"✅ Deleted {emp['emp_name']}")
                        st.rerun()
            else:
                st.info("No employees found.")

    # ── ADD COURSE ────────────────────────────────────────
    elif menu == "📚 Add Course":
        st.title("Add Course")
        with st.form("course_form"):
            name   = st.text_input("Course Name")
            fees   = st.number_input(
                "Course Fees (₹)",
                min_value=300,
                max_value=150000,
                value=5000,
                step=500
            )
            submit = st.form_submit_button("Add Course")
        if submit:
            if not name:
                st.warning("⚠️ Please enter course name")
            else:
                res = requests.post(f"{API}/courses", json={
                    "co_name": name, "co_fees": fees
                })
                if res.status_code == 200:
                    st.success(f"✅ Course added! {name} — ₹{fees}")
                else:
                    st.error("❌ Failed to add course")

    # ── MANAGE COURSES ────────────────────────────────────
    elif menu == "📚 Manage Courses":
        st.title("Manage Courses")
        if st.session_state.edit_course:
            c = st.session_state.edit_course
            st.subheader(f"✏️ Edit Course — {c['co_name']}")
            with st.form("edit_course_form"):
                e_name = st.text_input("Course Name", c["co_name"])
                e_fees = st.number_input(
                    "Course Fees (₹)",
                    min_value=300,
                    max_value=150000,
                    value=int(c["co_fees"]),
                    step=500
                )
                col_s, col_c = st.columns(2)
                save   = col_s.form_submit_button("💾 Save Changes")
                cancel = col_c.form_submit_button("❌ Cancel")
            if save:
                res = requests.put(
                    f"{API}/courses/{c['co_id']}", json={
                        "co_name": e_name,
                        "co_fees": e_fees
                    }
                )
                if res.status_code == 200:
                    st.success("✅ Course updated!")
                    st.session_state.edit_course = None
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {res.text}")
            if cancel:
                st.session_state.edit_course = None
                st.rerun()
        else:
            courses = requests.get(f"{API}/courses").json()
            if courses:
                cols = st.columns([1, 4, 2, 1, 1])
                for col, h in zip(cols, [
                    "ID", "Course Name", "Fees", "Edit", "Del"
                ]):
                    col.markdown(f"**{h}**")
                st.markdown("---")
                for c in courses:
                    cols = st.columns([1, 4, 2, 1, 1])
                    cols[0].write(c["co_id"])
                    cols[1].write(c["co_name"])
                    cols[2].write(f"₹{c['co_fees']}")
                    if cols[3].button("✏️", key=f"edit_course_{c['co_id']}"):
                        st.session_state.edit_course = c
                        st.rerun()
                    if cols[4].button("🗑️", key=f"del_course_{c['co_id']}"):
                        requests.delete(f"{API}/courses/{c['co_id']}")
                        st.success(f"✅ Deleted {c['co_name']}")
                        st.rerun()
            else:
                st.info("No courses found.")

    # ── ADD BATCH ─────────────────────────────────────────
    elif menu == "📦 Add Batch":
        st.title("Add Batch")
        courses    = requests.get(f"{API}/courses").json()
        course_map = {c["co_name"]: c["co_id"] for c in courses}
        with st.form("batch_form"):
            col1, col2 = st.columns(2)
            with col1:
                bt_number = st.text_input("Batch Number")
                bt_course = st.selectbox("Course Name", list(course_map.keys()))
            with col2:
                bt_from_date = st.date_input("From Date")
                bt_to_date   = st.date_input("To Date")
            submit = st.form_submit_button("Add Batch")
        if submit:
            res = requests.post(f"{API}/batches", json={
                "bt_number":    bt_number,
                "bt_course_id": course_map[bt_course],
                "bt_from_date": str(bt_from_date),
                "bt_to_date":   str(bt_to_date)
            })
            if res.status_code == 200:
                st.success("✅ Batch added!")
            else:
                st.error("❌ Failed to add batch")

    # ── MANAGE BATCHES ────────────────────────────────────
    elif menu == "📦 Manage Batches":
        st.title("Manage Batches")
        if st.session_state.edit_batch:
            b = st.session_state.edit_batch
            st.subheader(f"✏️ Edit Batch — {b['bt_number']}")
            courses    = requests.get(f"{API}/courses").json()
            course_map = {c["co_name"]: c["co_id"] for c in courses}
            course_names = list(course_map.keys())
            cur_course = next(
                (c["co_name"] for c in courses
                 if c["co_id"] == b["bt_course_id"]), course_names[0]
            )
            with st.form("edit_batch_form"):
                col1, col2 = st.columns(2)
                with col1:
                    e_number = st.text_input("Batch Number", b["bt_number"])
                    e_course = st.selectbox(
                        "Course Name",
                        course_names,
                        index=course_names.index(cur_course)
                    )
                with col2:
                    e_from = st.text_input(
                        "From Date", b.get("bt_from_date", "")
                    )
                    e_to   = st.text_input(
                        "To Date", b.get("bt_to_date", "")
                    )
                col_s, col_c = st.columns(2)
                save   = col_s.form_submit_button("💾 Save Changes")
                cancel = col_c.form_submit_button("❌ Cancel")
            if save:
                res = requests.put(
                    f"{API}/batches/{b['bt_id']}", json={
                        "bt_number":    e_number,
                        "bt_course_id": course_map[e_course],
                        "bt_from_date": e_from,
                        "bt_to_date":   e_to
                    }
                )
                if res.status_code == 200:
                    st.success("✅ Batch updated!")
                    st.session_state.edit_batch = None
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {res.text}")
            if cancel:
                st.session_state.edit_batch = None
                st.rerun()
        else:
            batches = requests.get(f"{API}/batches").json()
            if batches:
                cols = st.columns([1, 2, 3, 2, 2, 1, 1])
                for col, h in zip(cols, [
                    "ID", "Batch No", "Course",
                    "From", "To", "Edit", "Del"
                ]):
                    col.markdown(f"**{h}**")
                st.markdown("---")
                for b in batches:
                    cols = st.columns([1, 2, 3, 2, 2, 1, 1])
                    cols[0].write(b["bt_id"])
                    cols[1].write(b["bt_number"])
                    cols[2].write(b["co_name"])
                    cols[3].write(b.get("bt_from_date", ""))
                    cols[4].write(b.get("bt_to_date", ""))
                    if cols[5].button("✏️", key=f"edit_batch_{b['bt_id']}"):
                        st.session_state.edit_batch = b
                        st.rerun()
                    if cols[6].button("🗑️", key=f"del_batch_{b['bt_id']}"):
                        requests.delete(f"{API}/batches/{b['bt_id']}")
                        st.success(f"✅ Deleted {b['bt_number']}")
                        st.rerun()
            else:
                st.info("No batches found.")

    # ── REGISTER STUDENT ──────────────────────────────────
    elif menu == "🎓 Register Student":
        st.title("Register Student")
        courses    = requests.get(f"{API}/courses").json()
        course_map = {
            c["co_name"]: {"id": c["co_id"], "fees": c["co_fees"]}
            for c in courses
        }
        with st.form("student_form"):
            col1, col2 = st.columns(2)
            with col1:
                st_id      = st.text_input("Student ID")
                st_name    = st.text_input("Student Name")
                st_mobile  = st.text_input("Mobile Number")
                st_college = st.text_input("College Name")
            with col2:
                st_course  = st.selectbox("Course", list(course_map.keys()))
                auto_fees  = course_map[st_course]["fees"]
                st.info(f"💰 Course Fees: ₹{auto_fees}")
                batches    = requests.get(
                    f"{API}/batches/by-course/"
                    f"{course_map[st_course]['id']}"
                ).json()
                batch_map  = {b["bt_number"]: b["bt_id"] for b in batches}
                st_batch   = st.selectbox(
                    "Batch Number",
                    list(batch_map.keys()) if batch_map else ["No batches"]
                )
                st_ref = st.text_input("Reference Number")
            submit = st.form_submit_button("Register & Pay")
        if submit:
            if not st_id:
                st.warning("⚠️ Please enter Student ID")
            elif not st_name:
                st.warning("⚠️ Please enter Student Name")
            elif batch_map:
                res = requests.post(f"{API}/students", json={
                    "st_id":           st_id,
                    "st_name":         st_name,
                    "st_mobile":       st_mobile,
                    "st_college_name": st_college,
                    "st_fees":         auto_fees,
                    "st_batch_id":     batch_map[st_batch],
                    "st_ref_number":   st_ref
                })
                if res.status_code == 200:
                    st.success(
                        f"✅ Student {st_name} registered! "
                        f"ID: {st_id} | Fees: ₹{auto_fees}"
                    )
                    show_payment(auto_fees, st_name)
                elif res.status_code == 400:
                    st.error("❌ Student ID already exists!")
                else:
                    st.error(f"❌ Failed: {res.text}")
            else:
                st.warning("⚠️ Add a batch for this course first.")

    # ── VIEW STUDENTS ─────────────────────────────────────
    elif menu == "📋 View Students":
        st.title("All Students")
        if st.session_state.edit_student:
            s = st.session_state.edit_student
            st.subheader(f"✏️ Edit Student — {s['st_name']}")
            all_batches = requests.get(f"{API}/batches").json()
            batch_map   = {
                b["bt_number"]: b["bt_id"] for b in all_batches
            }
            cur_batch = next(
                (b["bt_number"] for b in all_batches
                 if b["bt_id"] == s["st_batch_id"]), None
            )
            with st.form("edit_student_form"):
                col1, col2 = st.columns(2)
                with col1:
                    e_name    = st.text_input("Student Name",  s["st_name"])
                    e_mobile  = st.text_input("Mobile Number", s.get("st_mobile", ""))
                    e_college = st.text_input("College Name",  s.get("st_college_name", ""))
                with col2:
                    e_fees = st.number_input(
                        "Fees", min_value=0.0,
                        value=float(s.get("st_fees", 0))
                    )
                    e_ref  = st.text_input(
                        "Reference Number",
                        s.get("st_ref_number", "")
                    )
                    batch_names = list(batch_map.keys())
                    e_batch = st.selectbox(
                        "Batch",
                        batch_names,
                        index=batch_names.index(cur_batch)
                        if cur_batch in batch_names else 0
                    )
                col_s, col_c = st.columns(2)
                save   = col_s.form_submit_button("💾 Save Changes")
                cancel = col_c.form_submit_button("❌ Cancel")
            if save:
                res = requests.put(
                    f"{API}/students/{s['st_id']}", json={
                        "st_id":           s["st_id"],
                        "st_name":         e_name,
                        "st_mobile":       e_mobile,
                        "st_college_name": e_college,
                        "st_fees":         e_fees,
                        "st_batch_id":     batch_map[e_batch],
                        "st_ref_number":   e_ref
                    }
                )
                if res.status_code == 200:
                    st.success("✅ Student updated!")
                    st.session_state.edit_student = None
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {res.text}")
            if cancel:
                st.session_state.edit_student = None
                st.rerun()
        else:
            students = requests.get(f"{API}/students").json()
            if students:
                cols = st.columns([1, 2, 2, 2, 2, 2, 2, 2, 1, 1])
                for col, h in zip(cols, [
                    "St ID", "Name", "Mobile", "Fees",
                    "College", "Ref No", "Batch",
                    "Course", "Edit", "Del"
                ]):
                    col.markdown(f"**{h}**")
                st.markdown("---")
                for s in students:
                    cols = st.columns([1, 2, 2, 2, 2, 2, 2, 2, 1, 1])
                    cols[0].write(s["st_id"])
                    cols[1].write(s["st_name"])
                    cols[2].write(s.get("st_mobile", ""))
                    cols[3].write(f"₹{s.get('st_fees', 0)}")
                    cols[4].write(s.get("st_college_name", ""))
                    cols[5].write(s.get("st_ref_number", ""))
                    cols[6].write(s["bt_number"])
                    cols[7].write(s["co_name"])
                    if cols[8].button("✏️", key=f"edit_stu_{s['st_id']}"):
                        st.session_state.edit_student = s
                        st.rerun()
                    if cols[9].button("🗑️", key=f"del_stu_{s['st_id']}"):
                        requests.delete(f"{API}/students/{s['st_id']}")
                        st.success(f"✅ Deleted {s['st_name']}")
                        st.rerun()
            else:
                st.info("No students registered yet.")

# ─── MAIN ─────────────────────────────────────────────────
if st.session_state.logged_in:
    admin_dashboard()
else:
    login_page()