import logging
from http import HTTPStatus
from typing import Union

from starlette.responses import Response
from starlette.requests import Request, HTTPConnection
from starlette_context.middleware import RawContextMiddleware
from starlette_context.errors import MiddleWareValidationError


from services.query import Query
from utils.tokens import validate_token


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AccessTokenMiddleware(RawContextMiddleware):
    async def set_context(self, request: Union[Request, HTTPConnection]) -> dict:
        url_path = request.url.path.lower()
        operation_name = request.headers.get("Operation-name")
        if url_path in ["/health"] or operation_name in ["Signup", "Token"]:
            return {}
        auth_token = request.headers.get("Authorization").split('Bearer ')[1]
        if auth_token:
            token_decoded = validate_token(auth_token)
            if token_decoded:
                log = Query()
                is_valid = (log.resolve_get_availablity("info", token_decoded)).get(
                    "is_available"
                )
                if not is_valid:
                    raise MiddleWareValidationError(
                        error_response=Response(
                            status_code=HTTPStatus.BAD_REQUEST,
                            content="App not available in DB.",
                        )
                    )
            else:
                raise MiddleWareValidationError(
                    error_response=Response(
                        status_code=HTTPStatus.BAD_REQUEST,
                        content="Couldn't validate token.",
                    )
                )
        else:
            raise MiddleWareValidationError(
                error_response=Response(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content="Token not provided in Headers.",
                )
            )
