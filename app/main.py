from fastapi import FastAPI
from app.exceptions.handlers import add_exception_handlers

from app.routes import project_routes, board_routes, user_routes

app = FastAPI()

app.include_router(project_routes.router)
app.include_router(board_routes.router)
app.include_router(user_routes.router)
add_exception_handlers(app)
