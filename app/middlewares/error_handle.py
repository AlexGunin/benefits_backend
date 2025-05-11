from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.exceptions import NotFoundError, DatabaseError
from sqlalchemy.exc import IntegrityError


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except NotFoundError as e:
            return JSONResponse(
                status_code=404,
                content={"detail": str(e)}
            )

        except DatabaseError as e:
            return JSONResponse(
                status_code=500,
                content={"detail": str(e)}
            )

        except IntegrityError as e:
            return JSONResponse(
                status_code=400,
                content={"detail": f"Integrity error: {str(e)}"}
            )

        except Exception as e:
            # 🔥 Если произошло что-то неожиданное
            return JSONResponse(
                status_code=500,
                content={"detail": f"Unexpected server error: {str(e)}"}
            )