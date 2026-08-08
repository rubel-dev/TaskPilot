import time
import logging
logger = logging.getLogger(__name__)
async def logging_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{duration: .2f}s"
    )
    return response
