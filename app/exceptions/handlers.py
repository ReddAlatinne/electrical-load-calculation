from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.errors import(
    ExistingProjectNameError,
    ProjectNotFoundError,
    BoardNotFoundError,
    NotProjectOwnerError,
    NotBoardProjectError,
    ExistingBoardNameError,
    InvalidCredentials,
    ExistingEmailError,
)


def add_exception_handlers(app: FastAPI):

    @app.exception_handler(ExistingProjectNameError)
    async def existing_project_name_handler(request: Request, exc: ExistingProjectNameError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Project name already exists for this user"},
        )

    @app.exception_handler(ProjectNotFoundError)
    async def project_not_found_handler(request: Request, exc: ProjectNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": "No existing project found under given id"},
        )

    @app.exception_handler(BoardNotFoundError)
    async def board_not_found_handler(request: Request, exc: BoardNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": "No existing board found under given id"},
        )

    @app.exception_handler(NotProjectOwnerError)
    async def not_project_owner_handler(request: Request, exc: NotProjectOwnerError):
        return JSONResponse(
            status_code=403,
            content={"detail": "User does not own this project"},
        )

    @app.exception_handler(NotBoardProjectError)
    async def not_board_Project_handler(request: Request, exc: NotBoardProjectError):
        return JSONResponse(
            status_code=403,
            content={"detail": "Board is not part of given project"},
        )

    @app.exception_handler(ExistingBoardNameError)
    async def existing_board_name_handler(request: Request, exc: ExistingBoardNameError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Board name already exists for this project"},
        )

    @app.exception_handler(InvalidCredentials)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentials):
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid credentials"},
        )

    @app.exception_handler(ExistingEmailError)
    async def existing_email_handler(request: Request, exc: ExistingEmailError):
        return JSONResponse(
            status_code=409,
            content={"detail": "Email already exists"},
        )