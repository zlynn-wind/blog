class APIError(Exception):

    def __init__(self, code, error, http_status=400):
        self.code = code
        self.error = error
        self.http_status = http_status

