from dataclasses import dataclass
import logging
from mediapipe.python.solutions.pose

@dataclass
class Gesture(PoseLandmark.Type):
  visible: bool

class MyRecognizerGestures:
  def __init__(self):
    self.log = logging.getLogger(__name__)
  
  def analyze(self):
    pass

  def __consider_gesture__(self, landmark):
    pass