from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


from app.routes.health import router as health_router
from app.routes.tasks import router as tasks_router
from app.routes.transaction import router as finance_router
from app.routes.budgets import router as budget_router
from app.routes.dashboard import router as dashboard_router

app = FastAPI(title="AthleteOps API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(tasks_router)
app.include_router(health_router)
app.include_router(finance_router)
app.include_router(budget_router)
app.include_router(dashboard_router)
