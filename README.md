****# 🎓 Admission Management System****************************

A full-stack web application to manage student admissions,
employees, courses, and batches for an institute.

---

## 🚀 Tech Stack

| Layer    | Technology        | Purpose                    |
|----------|-------------------|----------------------------|
| Frontend | Streamlit         | Web UI (port 8501)         |
| Backend  | FastAPI           | REST API (port 8000)       |
| Database | SQLite            | Data storage (admission.db)|
| Language | Python 3.12       | All layers                 |

---

## 📁 Project Structure

admission_system/
├── backend/
│   ├── main.py            ← FastAPI app + all API endpoints
│   ├── database.py        ← SQLite connection + auto DB creation
│   ├── models.py          ← Pydantic request models
│   ├── create_db.py       ← Manual database creation script
│   ├── fix_batches.py     ← Fix duplicate batches script
│   ├── reset_password.py  ← Reset admin password script
│   ├── test_db.py         ← Test database connection script
│   ├── view_data.py       ← View all database data script
│   └── admission.db       ← SQLite database file (auto created)
└── frontend/
└── app.py             ← Streamlit UI

---

## 🗄️ Database Schema

### roles
| Column  | Type    | Description        |
|---------|---------|--------------------|
| rl_id   | INTEGER | Primary Key        |
| rl_name | TEXT    | Role name          |

### employee
| Column           | Type    | Description           |
|------------------|---------|-----------------------|
| emp_id           | INTEGER | Primary Key           |
| emp_name         | TEXT    | Employee full name    |
| emp_comp_id      | TEXT    | Company ID (unique)   |
| emp_email        | TEXT    | Email address         |
| emp_mobile       | TEXT    | Mobile number         |
| emp_date_of_join | TEXT    | Date of joining       |
| emp_username     | TEXT    | Login username        |
| emp_password     | TEXT    | Login password        |
| emp_role         | INTEGER | FK → roles.rl_id      |

### course
| Column  | Type    | Description     |
|---------|---------|-----------------|
| co_id   | INTEGER | Primary Key     |
| co_name | TEXT    | Course name     |
| co_fees | REAL    | Course fees (₹) |

### batches
| Column       | Type    | Description        |
|--------------|---------|--------------------|
| bt_id        | INTEGER | Primary Key        |
| bt_number    | TEXT    | Batch number       |
| bt_course_id | INTEGER | FK → course.co_id  |
| bt_from_date | TEXT    | Batch start date   |
| bt_to_date   | TEXT    | Batch end date     |

### students
| Column         | Type | Description          |
|----------------|------|----------------------|
| st_id          | TEXT | Primary Key (manual) |
| st_name        | TEXT | Student full name    |
| st_mobile      | TEXT | Mobile number        |
| st_college_name| TEXT | College name         |
| st_fees        | REAL | Fees amount (₹)      |
| st_batch_id    | INT  | FK → batches.bt_id   |
| st_ref_number  | TEXT | Payment reference    |

---

## ⚙️ Installation & Setup

### Step 1 — Install Python packages
```bash
pip install fastapi uvicorn streamlit requests
```

### Step 2 — Create database
```bash
cd backend
python create_db.py
```

### Step 3 — Start Backend
```bash
cd backend
python -m uvicorn main:app --reload
```

### Step 4 — Start Frontend (new terminal)
```bash
cd frontend
python -m streamlit run app.py
```

### Step 5 — Open browser
http://localhost:8501


---

## 🔐 Default Login

| Field    | Value    |
|----------|----------|
| Username | admin    |
| Password | admin123 |
| Role     | Admin    |

---

## 📡 API Endpoints

### Auth
| Method | URL     | Description       |
|--------|---------|-------------------|
| POST   | /login  | Login with credentials |

### Roles
| Method | URL     | Description   |
|--------|---------|---------------|
| GET    | /roles  | Get all roles |

### Courses
| Method | URL              | Description      |
|--------|------------------|------------------|
| GET    | /courses         | Get all courses  |
| POST   | /courses         | Add new course   |
| PUT    | /courses/{id}    | Update course    |
| DELETE | /courses/{id}    | Delete course    |

### Batches
| Method | URL                        | Description           |
|--------|----------------------------|-----------------------|
| GET    | /batches                   | Get all batches       |
| GET    | /batches/by-course/{id}    | Get batches by course |
| POST   | /batches                   | Add new batch         |
| PUT    | /batches/{id}              | Update batch          |
| DELETE | /batches/{id}              | Delete batch          |

### Employees
| Method | URL               | Description        |
|--------|-------------------|--------------------|
| GET    | /employees        | Get all employees  |
| POST   | /employees        | Add new employee   |
| PUT    | /employees/{id}   | Update employee    |
| DELETE | /employees/{id}   | Delete employee    |

### Students
| Method | URL               | Description         |
|--------|-------------------|---------------------|
| GET    | /students         | Get all students    |
| POST   | /students         | Register student    |
| PUT    | /students/{id}    | Update student      |
| DELETE | /students/{id}    | Delete student      |

---

## 🖥️ Features

### 📊 Dashboard
- Total students count
- Total courses count
- Total batches count

### 👨‍💼 Employee Management
- Add employee with company ID, email, mobile, role
- View all employees in table
- Edit employee details
- Delete employee

### 📚 Course Management
- Add course with fees (min ₹300)
- View all courses with fees
- Edit course name and fees
- Delete course

### 📦 Batch Management
- Add batch with from/to dates
- Link batch to course
- View all batches
- Edit batch details
- Delete batch

### 🎓 Student Registration
- Register student with ID, name, mobile, college
- Auto display course fees on course selection
- Cascading course → batch dropdown
- UPI QR code payment after registration

### 💳 Payment System
- Auto generate UPI QR code
- Display UPI ID for manual payment
- Support GPay, PhonePe, Paytm

### 🔐 Login System
- Username and password login
- Role based access
- Session management
- Logout button

---

## 🛠️ Utility Scripts

| Script             | Command                      | Purpose                    |
|--------------------|------------------------------|----------------------------|
| create_db.py       | python create_db.py          | Create fresh database      |
| test_db.py         | python test_db.py            | Test DB and show all data  |
| fix_batches.py     | python fix_batches.py        | Fix duplicate batches      |
| reset_password.py  | python reset_password.py     | Reset admin password       |
| view_data.py       | python view_data.py          | View all data in terminal  |

---

## 🏗️ Architecture

Browser (localhost:8501)
↓
Streamlit Frontend (app.py)
↓ HTTP requests
FastAPI Backend (main.py)
↓ SQL queries
SQLite Database (admission.db)

---

## 🔄 How to Run (Quick Reference)

```bash
# Terminal 1 — Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2 — Frontend
cd frontend
python -m streamlit run app.py
```

---

## 🌐 URLs

| Service       | URL                          |
|---------------|------------------------------|
| Frontend      | http://localhost:8501        |
| Backend API   | http://127.0.0.1:8000        |
| API Docs      | http://127.0.0.1:8000/docs   |

---

## 💡 Troubleshooting

| Problem                  | Solution                          |
|--------------------------|-----------------------------------|
| Backend not starting     | Check MySQL/SQLite installed      |
| Frontend can't connect   | Start backend first               |
| Login not working        | Run reset_password.py             |
| Tables not found         | Run create_db.py                  |
| Duplicate batches        | Run fix_batches.py                |
| Port already in use      | Restart terminal and try again    |

---

## 👨‍💻 Developer

- **Project:** Admission Management System
- **Language:** Python 3.12
- **Database:** SQLite
- **Framework:** FastAPI + Streamlit

---

## 📄 License

This project is built for internship/educational purposes.

