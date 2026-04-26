from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class EmployeeCreate(BaseModel):
    emp_name: str
    emp_comp_id: str
    emp_email: Optional[str] = None
    emp_mobile: Optional[str] = None
    emp_date_of_join: Optional[str] = None
    emp_username: str
    emp_password: str
    emp_role: int

class CourseCreate(BaseModel):
    co_name: str
    co_fees: float = 0

class BatchCreate(BaseModel):
    bt_number: str
    bt_course_id: int
    bt_from_date: Optional[str] = None
    bt_to_date: Optional[str] = None

class StudentCreate(BaseModel):
    st_id: str
    st_name: str
    st_mobile: Optional[str] = None
    st_college_name: Optional[str] = None
    st_fees: Optional[float] = 0
    st_batch_id: int
    st_ref_number: Optional[str] = None