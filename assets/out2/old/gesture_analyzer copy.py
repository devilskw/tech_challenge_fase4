from cv2.typing import MatLike
from mediapipe.python.solutions.holistic import Holistic
import mediapipe.python.solutions.drawing_utils as mp_draw_utils
from mediapipe.python.solutions import holistic

from pos_ai_video_analyzer.analyzers import Analyzer
from pos_ai_video_analyzer.video_properties import VideoProperties

class GestureAnalyzer(Analyzer):
  def __init__(self, config: dict, video_property: VideoProperties):
    super().__init__(config, video_property)

  def analyze(self, frame, id_frame, image):
    self.log.info(f"Analisando gestos do frame {id_frame} do vídeo.")
    with Holistic(min_detection_confidence=self.cfg['min_detection_confidence']) as detection:
      result = detection.process(image)
      gestures = []

      if result.pose_landmarks:
        self.__draw_landmarks__(frame, id_frame, result.pose_landmarks, holistic.POSE_CONNECTIONS)

      # if result.pose_world_landmarks:
      #   self.__draw_landmarks__(frame, id_frame, result.pose_world_landmarks, holistic.POSE_CONNECTIONS)

      # if result.left_hand_landmarks:
      #   self.__draw_landmarks__(frame, id_frame, result.left_hand_landmarks, holistic.HAND_CONNECTIONS)

      # if result.right_hand_landmarks:
      #   self.__draw_landmarks__(frame, id_frame, result.right_hand_landmarks, holistic.HAND_CONNECTIONS)

      gestures.append({
          'id_frame': id_frame
        , 'gestures': result.pose_landmarks.landmark
      })



      # if result.detections:
      #   self.log.debug(f"Encontrados {len(result.detections)} possíveis gestos no frame {id_frame}.")
      #   id_gesture = 0
      #   for detection in result.detections:
      #     id_gesture += 1
      #     x, y, w, h = self.__get_pose_box_positions__(frame, detection)
      #     identified_gestures = self.__analyze_gestures_detection__(frame, detection, id_frame, id_gesture)
      #     gestures.append({
      #         'id_frame': id_frame
      #       , 'id_gesture': id_gesture
      #       , 'gestures': identified_gestures
      #       , 'pos_x': x
      #       , 'pos_y': y
      #       , 'width': w
      #       , 'height': h
      #     })
      #   self.__draw_landmarks__(frame, id_frame, result.right_hand_landmarks, holistic.HAND_CONNECTIONS, id_gesture)
      #   self.__draw_landmarks__(frame, id_frame, result.left_hand_landmarks, holistic.HAND_CONNECTIONS,id_gesture)
      #   self.__draw_landmarks__(frame, id_frame, result.pose_landmarks, holistic.POSE_CONNECTIONS, id_gesture)
    return frame, gestures

  def __draw_landmarks__(self, frame: MatLike, id_frame, detections, conn: frozenset):
    self.log.debug(f"Desenhando landmark dos gestos {conn} no frame {id_frame}.")
    mp_draw_utils.draw_landmarks(frame, detections, conn)



  # def __get_pose_box_positions__(self, frame: MatLike, detection) -> MatLike:
  #   height, width, _ = frame.shape
  #   box = detection.location_data.relative_bounding_box
  #   bbox = int(box.xmin * width), int(box.ymin * height), int(box.width * width), int(box.height * height)
  #   return bbox

  # def __analyze_gestures_detection__(self, frame, detection, id_frame, id_gesture):
  #   self.log.debug(f"Analisando gestos {id_gesture} no frame {id_frame}.")
  #   self.log.info("id_frame")
  #   self.log.info(id_frame)
  #   self.log.info("frame")
  #   self.log.info(frame)
  #   self.log.info("detection")
  #   self.log.info(detection)
  #   return []