import http

from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

from app.domain.exceptions.invalid_password_error import InvalidPasword
from app.domain.exceptions.user_already_exist_error import UserAreadyExists
from app.domain.exceptions.user_not_found_error import UserNotFound
from app.domain.exceptions.user_registration_error import UserRegistrationError


async def response_unauthorized_exception(
    request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=http.HTTPStatus.BAD_REQUEST,
        content={"message": str(exc)},
    )


async def response_bad_request_exception(
    request: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=http.HTTPStatus.BAD_REQUEST,
        content={"message": str(exc)},
    )


async def response_not_found_exception(
    _equest: Request, exc: Exception
) -> JSONResponse:
    return JSONResponse(
        status_code=http.HTTPStatus.NOT_FOUND,
        content={"message": str(exc)},
    )


def exception_handlers(app: FastAPI):
    app.exception_handler(InvalidPasword)(response_unauthorized_exception)
    app.exception_handler(UserAreadyExists)(response_bad_request_exception)
    app.exception_handler(UserNotFound)(response_not_found_exception)
    app.exception_handler(UserRegistrationError)(response_bad_request_exception)
