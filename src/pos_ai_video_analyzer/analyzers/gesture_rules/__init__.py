
from mediapipe.python.solutions.pose import PoseLandmark

from pos_ai_video_analyzer.analyzers.gesture_rules.rules import *


class GestureRules:
  gesture_rules: list[GestureRule] = []
  def __init__(self):
    self.gesture_rules.append(RegraBracoLevantado())
    self.gesture_rules.append(RegraDeitado())

  def identify_gestures(self, lndmk) -> list[GestureRuleResult]:
    gestures = []
    for gesture_rule in self.gesture_rules:
      rule = gesture_rule.validate(lndmk)
      if rule.is_valid(): gestures.append(rule)
    return gestures


