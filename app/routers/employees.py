from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from typing import Optional
import db

router = APIRouter(prefix="/employees")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
def list_employees(request: Request):
    employees = db.query("""
        SELECT e.employee_id, e.first_name, e.last_name, e.email, e.phone,
               j.title AS current_job, d.name AS current_dept
        FROM employees e
        LEFT JOIN LATERAL (
            SELECT job_id, department_id FROM job_history
            WHERE employee_id = e.employee_id AND termination_date IS NULL
            ORDER BY hire_date DESC LIMIT 1
        ) jh ON true
        LEFT JOIN jobs j ON j.job_id = jh.job_id
        LEFT JOIN departments d ON d.department_id = jh.department_id
        ORDER BY e.last_name, e.first_name
    """)
    return templates.TemplateResponse(
        "employees/list.html", {"request": request, "employees": employees}
    )


@router.get("/new", response_class=HTMLResponse)
def new_form(request: Request):
    return templates.TemplateResponse(
        "employees/_form.html", {"request": request, "employee": None}
    )


@router.get("/{employee_id}/edit", response_class=HTMLResponse)
def edit_form(employee_id: int, request: Request):
    employee = db.query_one(
        "SELECT * FROM employees WHERE employee_id = %s", (employee_id,)
    )
    return templates.TemplateResponse(
        "employees/_form.html", {"request": request, "employee": employee}
    )


@router.post("", response_class=Response)
def create(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
):
    db.execute(
        "INSERT INTO employees (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)",
        (first_name, last_name, email, phone or None),
    )
    return Response(status_code=204, headers={"HX-Redirect": "/employees"})


@router.put("/{employee_id}", response_class=Response)
def update(
    employee_id: int,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
):
    db.execute(
        "UPDATE employees SET first_name=%s, last_name=%s, email=%s, phone=%s WHERE employee_id=%s",
        (first_name, last_name, email, phone or None, employee_id),
    )
    return Response(status_code=204, headers={"HX-Redirect": "/employees"})


@router.delete("/{employee_id}", response_class=Response)
def delete(employee_id: int):
    db.execute("DELETE FROM employees WHERE employee_id = %s", (employee_id,))
    return Response(status_code=200)
