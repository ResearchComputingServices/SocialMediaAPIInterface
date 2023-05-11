from .setup_logger import logger
from .comments import Comments
from .videos import Videos
from .channels import Channels


class Youtube:
    def __init__(self, api_key) -> None:
        logger.debug("Initializing object.")
        self.comments = Comments(self)
        self.videos = Videos(self)
        self.channels = Channels(self)
        self._apikey = api_key

    def login(self):
        logger.debug(f"Should login using the api_key {self._apikey}")
        
