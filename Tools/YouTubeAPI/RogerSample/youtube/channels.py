import logging
from . import setup_logger

logger = logging.getLogger('youtube.channels')

class Channels:
    def __init__(self, youtube) -> None:
        logger.debug("Initializing module")
        self._youtube = youtube
        