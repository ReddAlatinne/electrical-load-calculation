from fastapi import FastAPI

from app.routes import project_routes

app = FastAPI()

app.include_router(project_routes.router)