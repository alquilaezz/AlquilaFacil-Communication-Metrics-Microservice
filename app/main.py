from fastapi import FastAPI
from .database import Base, engine
from .routers import metrics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Metrics Service")

app.include_router(metrics.router)
