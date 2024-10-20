import logging

from pos_ai_video_analyzer.video_properties import VideoProperties

class Analyzer:

  cfg: dict
  prop: VideoProperties

  def __init__(self, config: dict, video_property: VideoProperties):
    self.log = logging.getLogger(__name__)
    self.cfg = config
    self.prop = video_property
