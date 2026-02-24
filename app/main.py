from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import employees, departments, jobs, job_history

app = FastAPI(title="HR Manager")
templates = Jinja2Templates(directory="templates")

app.include_router(employees.router)
app.include_router(departments.router)
app.include_router(jobs.router)
app.include_router(job_history.router)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
