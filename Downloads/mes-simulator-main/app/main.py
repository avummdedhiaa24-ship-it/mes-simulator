from fastapi import FastAPI
from app.routers import orders, execution, quality, dashboard, machine, analytics

app = FastAPI(
    title="MES Simulator",
    version="1.0.0"
)

app.include_router(orders.router)
app.include_router(execution.router)
app.include_router(quality.router)
app.include_router(dashboard.router)
app.include_router(machine.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "MES Simulator API running"}
