import logging
from . import setup_logger

logger = logging.getLogger('youtube.comments')

class Comments(object):
    def __init__(self, youtube) -> None:
        logger.debug("Initializing object.")
        self._youtube = youtube
    
    def get_comments_for_ids(self, ids:list):
        logger.debug(f"Comments:get_comments_for_ids: ids {ids}")
        
        