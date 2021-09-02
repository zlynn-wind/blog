from http import HTTPStatus

from Blog.error import APIError


CODE_RANGE = (10000, 10999)

USER_NOT_FOUND = APIError(10001, "user not found", HTTPStatus.NOT_FOUND)
USER_ID_NOT_FOUND = APIError(10002, "user id not found", HTTPStatus.NOT_FOUND)
USER_NAME_NOT_FOUND = APIError(10003, "user name not found", HTTPStatus.NOT_FOUND)  # noqa
USER_WRONG_PASSWORD = APIError(10004, "user password is wrong", HTTPStatus.UNAUTHORIZED)  # noqa
