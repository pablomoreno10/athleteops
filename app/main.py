from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.routes.health import router as health_router
from app.routes.tasks import router as tasks_router
from app.routes.transaction import router as finance_router
from app.routes.budgets import router as budget_router
from app.routes.dashboard import router as dashboard_router
from app.routes.credentials import router as credentials_router
from app.routes.debug import router as debug_router

app = FastAPI(title="AthleteOps API")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    """Redirect root to login page."""
    return RedirectResponse(url="/auth/login")

app.include_router(tasks_router)
app.include_router(health_router)
app.include_router(finance_router)
app.include_router(budget_router)
app.include_router(dashboard_router)
app.include_router(credentials_router)
app.include_router(debug_router)
