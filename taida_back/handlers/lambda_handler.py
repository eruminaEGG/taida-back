from http import HTTPStatus
import json
import logging
from typing import Any, Callable, Dict, Tuple, TypeAlias

from taida_back.core.log import get_logger
from taida_back.exceptions import validation_exception

FunctionResponse: TypeAlias = Tuple[HTTPStatus, Any, Any]
Function: TypeAlias = Callable[[Dict[str, Any]], FunctionResponse]


def lambda_handler(func: Function):
    def _lambda_handler(event: Dict[str, Any], context: Any) -> Any:
        logger: logging.Logger = get_logger()()
        request_body: dict[str, Any] | None = None
        if event.get("body") is not None:
            request_body = json.loads(event["body"])
        logger.info(json.dumps({
            "body": request_body,
            "queryParams": event.get("queryStringParameters"),
            "pathParams": event.get("pathParameters"),
        }))

        response: Dict[str, Any] = {}

        # response のヘッダーを作成する
        # TODO ヘッダーをENVから取得するようにする
        headers: Dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,DELETE,PUT",
        }

        try:
            status_code, response_headers, response_body = func(event)

            if response_headers is not None:
                headers = {**headers, **response_headers, "Content-Type": "application/json"}

            body: str = ""
            if response_body is not None:
                if isinstance(response_body, str):
                    try:
                        response_body = json.loads(response_body)
                    except json.JSONDecodeError:
                        pass
                body = json.dumps(response_body, ensure_ascii=False, default=str)

            response = {
                "statusCode": status_code,
                "headers": headers,
                "body": body
            }
        except validation_exception as validate_e:
            logging.error(validate_e)
            response = {
                "statusCode": HTTPStatus.BAD_REQUEST,
                "headers": headers,
                "body": json.dumps(str(validate_e))
            }

        except Exception as e:
            logging.error(e)
            response = {
                "statusCode": HTTPStatus.INTERNAL_SERVER_ERROR,
                "headers": headers,
                "body": json.dumps(str(e))
            }

        logger.info(json.dumps(response))
        return response

    return _lambda_handler
