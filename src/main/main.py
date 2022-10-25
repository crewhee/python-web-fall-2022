from fastapi import FastAPI

from .routers import default_routes, rabbit_routes


app = FastAPI()
app.include_router(default_routes.router)
app.include_router(rabbit_routes.rabbit_router)