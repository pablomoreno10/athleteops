from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from app.routes.health import router as health_router
from app.routes.tasks import router as tasks_router
from app.routes.transaction import router as finance_router
from app.routes.budgets import router as budget_router

app = FastAPI(title="AthleteOps API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(tasks_router)
app.include_router(health_router)
app.include_router(finance_router)
app.include_router(budget_router)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})
