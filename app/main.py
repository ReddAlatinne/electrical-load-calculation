from fastapi import FastAPI
from app.exceptions.handlers import add_exception_handlers

from app.routes import project_routes

app = FastAPI()

app.include_router(project_routes.router)
add_exception_handlers(app)