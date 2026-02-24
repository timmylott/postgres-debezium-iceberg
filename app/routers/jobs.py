from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from typing import Optional
import db

router = APIRouter(prefix="/jobs")
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
def list_jobs(request: Request):
    jobs = db.query("SELECT * FROM jobs ORDER BY title")
    return templates.TemplateResponse(
        "jobs/list.html", {"request": request, "jobs": jobs}
    )


@router.get("/new", response_class=HTMLResponse)
def new_form(request: Request):
    return templates.TemplateResponse(
        "jobs/_form.html", {"request": request, "job": None}
    )


@router.get("/{job_id}/edit", response_class=HTMLResponse)
def edit_form(job_id: int, request: Request):
    job = db.query_one("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
    return templates.TemplateResponse(
        "jobs/_form.html", {"request": request, "job": job}
    )


@router.post("", response_class=Response)
def create(
    title: str = Form(...),
    min_salary: Optional[float] = Form(None),
    max_salary: Optional[float] = Form(None),
):
    db.execute(
        "INSERT INTO jobs (title, min_salary, max_salary) VALUES (%s, %s, %s)",
        (title, min_salary, max_salary),
    )
    return Response(status_code=204, headers={"HX-Redirect": "/jobs"})


@router.put("/{job_id}", response_class=Response)
def update(
    job_id: int,
    title: str = Form(...),
    min_salary: Optional[float] = Form(None),
    max_salary: Optional[float] = Form(None),
):
    db.execute(
        "UPDATE jobs SET title=%s, min_salary=%s, max_salary=%s WHERE job_id=%s",
        (title, min_salary, max_salary, job_id),
    )
    return Response(status_code=204, headers={"HX-Redirect": "/jobs"})


@router.delete("/{job_id}", response_class=Response)
def delete(job_id: int):
    db.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
    return Response(status_code=200)
