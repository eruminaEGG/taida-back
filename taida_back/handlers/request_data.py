from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class RequestData:
    auth: Dict[str, Any]
    body: Dict[str, Any]
    path_params: Dict[str, str]
    query_params: Dict[str, str]

    @classmethod
    def create(
        cls,
        request_dict: Dict[str, Any]
    ) -> "RequestData":
        return cls(
            auth=request_dict.get("auth", {}),
            body=request_dict.get("body", {}),
            path_params=request_dict.get("path_params", {}),
            query_params=request_dict.get("query_params", {}),
        )

    def flatten(self) -> Dict[str, Any]:
        return {
            **self.auth,
            **self.body,
            **self.path_params,
            **self.query_params,
        }
