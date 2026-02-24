from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from typing import Optional
import db

router = APIRouter(prefix="/employees/{employee_id}/job-history")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
def list_job_history(employee_id: int, request: Request):
    employee = db.query_one(
        "SELECT * FROM employees WHERE employee_id = %s", (employee_id,)
    )
    history = db.query("""
        SELECT jh.*, j.title AS job_title, d.name AS dept_name,
               m.first_name || ' ' || m.last_name AS manager_name
        FROM job_history jh
        JOIN jobs j ON j.job_id = jh.job_id
        JOIN departments d ON d.department_id = jh.department_id
        LEFT JOIN employees m ON m.employee_id = jh.manager_id
        WHERE jh.employee_id = %s
        ORDER BY jh.hire_date DESC
    """, (employee_id,))
    return templates.TemplateResponse("job_history/list.html", {
        "request": request,
        "employee": employee,
        "history": history,
    })


@router.get("/new", response_class=HTMLResponse)
def new_form(employee_id: int, request: Request):
    jobs = db.query("SELECT job_id, title FROM jobs ORDER BY title")
    departments = db.query("SELECT department_id, name FROM departments ORDER BY name")
    managers = db.query(
        "SELECT employee_id, first_name || ' ' || last_name AS name FROM employees ORDER BY last_name"
    )
    return templates.TemplateResponse("job_history/_form.html", {
        "request": request,
        "employee_id": employee_id,
        "entry": None,
        "jobs": jobs,
        "departments": departments,
        "managers": managers,
    })


@router.get("/{entry_id}/edit", response_class=HTMLResponse)
def edit_form(employee_id: int, entry_id: int, request: Request):
    entry = db.query_one("SELECT * FROM job_history WHERE id = %s", (entry_id,))
    jobs = db.query("SELECT job_id, title FROM jobs ORDER BY title")
    departments = db.query("SELECT department_id, name FROM departments ORDER BY name")
    managers = db.query(
        "SELECT employee_id, first_name || ' ' || last_name AS name FROM employees ORDER BY last_name"
    )
    return templates.TemplateResponse("job_history/_form.html", {
        "request": request,
        "employee_id": employee_id,
        "entry": entry,
        "jobs": jobs,
        "departments": departments,
        "managers": managers,
    })


@router.post("", response_class=Response)
def create(
    employee_id: int,
    job_id: int = Form(...),
    department_id: int = Form(...),
    manager_id: Optional[int] = Form(None),
    hire_date: str = Form(...),
    termination_date: Optional[str] = Form(None),
    salary: Optional[float] = Form(None),
    reason: Optional[str] = Form(None),
):
    db.execute("""
        INSERT INTO job_history
            (employee_id, job_id, department_id, manager_id, hire_date, termination_date, salary, reason)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (employee_id, job_id, department_id, manager_id, hire_date,
          termination_date or None, salary, reason or None))
    return Response(
        status_code=204,
        headers={"HX-Redirect": f"/employees/{employee_id}/job-history"},
    )


@router.put("/{entry_id}", response_class=Response)
def update(
    employee_id: int,
    entry_id: int,
    job_id: int = Form(...),
    department_id: int = Form(...),
    manager_id: Optional[int] = Form(None),
    hire_date: str = Form(...),
    termination_date: Optional[str] = Form(None),
    salary: Optional[float] = Form(None),
    reason: Optional[str] = Form(None),
):
    db.execute("""
        UPDATE job_history SET
            job_id=%s, department_id=%s, manager_id=%s,
            hire_date=%s, termination_date=%s, salary=%s, reason=%s
        WHERE id=%s
    """, (job_id, department_id, manager_id, hire_date,
          termination_date or None, salary, reason or None, entry_id))
    return Response(
        status_code=204,
        headers={"HX-Redirect": f"/employees/{employee_id}/job-history"},
    )


@router.delete("/{entry_id}", response_class=Response)
def delete(employee_id: int, entry_id: int):
    db.execute("DELETE FROM job_history WHERE id = %s", (entry_id,))
    return Response(status_code=200)
