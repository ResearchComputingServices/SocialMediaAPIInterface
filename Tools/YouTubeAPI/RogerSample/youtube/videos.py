import logging
from . import setup_logger

logger = logging.getLogger('youtube.videos')

class Videos:
    def __init__(self, youtube):
        logger.debug("Initializing object.")    
        self._youtube = youtube
    
    def get_videos_by_id(self, ids: list):
        logger.debug(f"get_videos_by_id: ids {ids}")
    
    def get_videos_for_file(self, file):
        logger.debug(f"get_videos_for_file: file {file}")