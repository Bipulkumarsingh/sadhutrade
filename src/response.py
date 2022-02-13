from typing import Dict, Tuple


class ResponseMeta(type):
    _instance = None

    def __call__(cls):
        if cls._instance is None:
            cls._instance = super().__call__()
        return cls._instance


class ResponseData(metaclass=ResponseMeta):
    def __init__(self):
        self.RESPONSE = {"version": {"version": "1.2.0.0", "name": "sadhuTrade"},
                         "status": {"code": 200, "value": "OK"},
                         "data": None, "error": False}
        self.HEADERS = {"content-type": "application/json",
                        "cache-control": "no-cache",
                        'Accept': 'application/json, text/plain, */*',
                        'Authorization': 'bearer '
                        }

    def format_response(self, status_value: Dict) -> Dict:
        self.RESPONSE["status"]["code"] = status_value["code"]
        self.RESPONSE["status"]["value"] = status_value["value"]
        self.RESPONSE["data"] = status_value["data"]
        self.RESPONSE["error"] = status_value.get("error", False)
        return self.RESPONSE

    def http_200(self, **kwargs) -> Tuple:
        """OK"""
        status = {
            "code": 200,
            "value": "Ok",
            "data": "Success"
        }
        status.update(kwargs)
        return self.format_response(status), 200

    def http_201(self, **kwargs) -> Tuple:
        """Created"""
        status = {
            "code": 201,
            "value": "Created"
        }
        status.update(kwargs)
        return self.format_response(status), 201

    def http_203(self, **kwargs) -> Tuple:
        """Non-Authoritative Information"""
        status = {
            "code": 203,
            "value": "Non-Authoritative Information"
        }
        status.update(kwargs)
        return self.format_response(status), 203

    def http_401(self, **kwargs) -> Tuple:
        """Unauthorized"""
        status = {
            "code": 401,
            "value": "Unauthorized"
        }
        status.update(kwargs)
        return self.format_response(status), 401

    def http_404(self, **kwargs) -> Tuple:
        """Not Found"""
        status = {
            "code": 404,
            "value": "Not Found"
        }
        status.update(kwargs)
        return self.format_response(status), 404

    def http_405(self, **kwargs) -> Tuple:
        """Not Allowed"""
        status = {
            "code": 405,
            "value": "Not Allowed",
            "data": "Method Not Allowed"
        }
        status.update(kwargs)
        return self.format_response(status), 405

    def http_406(self, **kwargs) -> Tuple:
        """Not Acceptable"""
        status = {
            "code": 406,
            "value": "Not Acceptable"
        }
        status.update(kwargs)
        return self.format_response(status), 406

    def http_409(self, **kwargs) -> Tuple:
        """Conflict"""
        status = {
            "code": 409,
            "value": "Conflict"
        }
        status.update(kwargs)
        return self.format_response(status), 409

    def http_500(self, **kwargs) -> Tuple:
        """Internal Server Error"""
        status = {
            "code": 500,
            "value": "Internal Server Error",
            "data": "Something went wrong"
        }
        status.update(kwargs)
        return self.format_response(status), 500

    def http_503(self, **kwargs) -> Tuple:
        """Service Unavailable"""
        status = {
            "code": 503,
            "value": "Service Unavailable",
            "data": "Service Not able to complete request."
        }
        status.update(kwargs)
        return self.format_response(status), 503
