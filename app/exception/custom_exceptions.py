class AppException(Exception):
    def __init__(
            self,
            message:str,
            status_code:int = 400,
            error_code:str = 'APP_ERROR'
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

class NotFoundException(AppException):
    def __init__(self, message:str = 'Resource Not Found'):
        super().__init__(
            message=message,
            status_code=404,
            error_code = 'NOT_FOUND'
        )

class InvalidCredentialsException(AppException):
    def __init__(self, message:str ='Resource Not Found'):
        super().__init__(
            message=message,
            status_code=400,
            error_code='Invalid Credentials'
        )
class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="UNAUTHORIZED"
        )

class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="FORBIDDEN"
        )