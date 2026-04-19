from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.errors import(
    ExistingProjectNameError
)


def add_exception_handlers(app: FastAPI):

    @app.exception_handler(ExistingProjectNameError)
    async def existing_project_name_handler(request: Request, exc: ExistingProjectNameError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Project name already exists for this user"},
        )