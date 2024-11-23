import os
import logging
from cv2.typing import MatLike

from pos_ai_video_analyzer.video_properties import VideoProperties

class Analyzer:

  cfg: dict
  filename: str
  path_out: str
  prop: VideoProperties

  def __init__(self, config: dict, base_path_out: str, path_prefix: str, filename: str, video_property: VideoProperties):
    self.log = logging.getLogger(__name__)
    self.cfg = config
    self.filename = filename
    self.path_out = base_path_out if path_prefix == '' else os.path.join(base_path_out, path_prefix)
    if not os.path.exists(self.path_out):
      os.makedirs(self.path_out)
    self.prop = video_property
