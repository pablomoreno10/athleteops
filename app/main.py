from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.tasks import router as tasks_router
from app.routes.transaction import router as finance_router
from app.routes.budgets import router as budget_router

app = FastAPI(title="AthleteOps API")

app.include_router(tasks_router)
app.include_router(health_router)
app.include_router(finance_router)
app.include_router(budget_router)

@app.get("/health", tags=["meta"])
def health_check():
    return {"status": "ok"}
