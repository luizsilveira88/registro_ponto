from rest_framework.response import Response
from rest_framework import status


class ResponseSuccess(Response):
    def __init__(self, msg, data=None, status_code=status.HTTP_200_OK):

        response_data = {
            "result": "success",
            "msg": msg,
        }

        if data is not None:
            response_data["data"] = data

        super().__init__(response_data, status=status_code)


class ResponseError(Response):
    def __init__(self, msg, error=None, status_code=status.HTTP_400_BAD_REQUEST):

        response_data = {
            "result": "error",
            "msg": msg,
        }

        if error is not None:
            response_data["error"] = error

        super().__init__(response_data, status=status_code)
