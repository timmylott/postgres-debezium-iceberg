from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from typing import Optional
import db

router = APIRouter(prefix="/departments")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
def list_departments(request: Request):
    departments = db.query(
        "SELECT * FROM departments ORDER BY name"
    )
    return templates.TemplateResponse(
        "departments/list.html", {"request": request, "departments": departments}
    )


@router.get("/new", response_class=HTMLResponse)
def new_form(request: Request):
    return templates.TemplateResponse(
        "departments/_form.html", {"request": request, "department": None}
    )


@router.get("/{department_id}/edit", response_class=HTMLResponse)
def edit_form(department_id: int, request: Request):
    department = db.query_one(
        "SELECT * FROM departments WHERE department_id = %s", (department_id,)
    )
    return templates.TemplateResponse(
        "departments/_form.html", {"request": request, "department": department}
    )


@router.post("", response_class=Response)
def create(
    name: str = Form(...),
    location: Optional[str] = Form(None),
):
    db.execute(
        "INSERT INTO departments (name, location) VALUES (%s, %s)",
        (name, location or None),
    )
    return Response(status_code=204, headers={"HX-Redirect": "/departments"})


@router.put("/{department_id}", response_class=Response)
def update(
    department_id: int,
    name: str = Form(...),
    location: Optional[str] = Form(None),
):
    db.execute(
        "UPDATE departments SET name=%s, location=%s WHERE department_id=%s",
        (name, location or None, department_id),
    )
    return Response(status_code=204, headers={"HX-Redirect": "/departments"})


@router.delete("/{department_id}", response_class=Response)
def delete(department_id: int):
    db.execute("DELETE FROM departments WHERE department_id = %s", (department_id,))
    return Response(status_code=200)
