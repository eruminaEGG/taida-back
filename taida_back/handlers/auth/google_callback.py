from http import HTTPStatus
from typing import Any, Dict

from taida_back.handlers.lambda_handler import lambda_handler


@lambda_handler
def exec(event: Dict[str, Any]):

    return HTTPStatus.OK, None, {"status": "OK"}
