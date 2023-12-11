from logging import getLogger

from uvicorn.config import LOGGING_CONFIG

logger = getLogger('uvicorn.app')
logger.setLevel("DEBUG") # 効かない？
LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"