from fastapi import FastAPI
from .routers import default_routes


app = FastAPI()
app.include_router(default_routes.router)
