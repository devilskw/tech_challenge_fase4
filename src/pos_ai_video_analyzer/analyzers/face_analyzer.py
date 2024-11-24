from cv2.typing import MatLike
from mediapipe.python.solutions.face_detection import FaceDetection
import mediapipe.python.solutions.drawing_utils as mp_draw_utils
from deepface import DeepFace

from pos_ai_video_analyzer.analyzers import Analyzer
from pos_ai_video_analyzer.video_properties import VideoProperties

class FaceAnalyzer(Analyzer):
  def __init__(self, config: dict, video_property: VideoProperties):
    super().__init__(config, video_property)

  def analyze(self, frame, id_frame, image):
    self.log.info(f"Analisando rostos do frame {id_frame} do vídeo.")
    with FaceDetection(min_detection_confidence=self.cfg['min_detection_confidence']) as detection:
      result = detection.process(image)
      faces = []
      if result.detections:
        self.log.debug(f"Encontrados {len(result.detections)} rostos no frame {id_frame}.")
        id_face = 0
        for detection in result.detections:
          id_face += 1
          x, y, w, h = self.__get_face_box_positions__(frame, detection)
          emotion = self.__analyze_face_detection__(frame, id_frame, id_face)
          faces.append({
              'id_frame': id_frame
            , 'id_face': id_face
            , 'emotion': emotion
            , 'pos_x': x
            , 'pos_y': y
            , 'width': w
            , 'height': h
          })
          self.__draw_landmarks__(frame, id_frame, detection, id_face)
    return frame, faces

  def __draw_landmarks__(self, frame: MatLike, id_frame, detection, id_face):
    self.log.debug(f"Desenhando landmark do rosto {id_face} no frame {id_frame}.")
    mp_draw_utils.draw_detection(frame, detection)

  def __analyze_face_detection__(self, frame, id_frame, id_face) -> str:
    emotion = "unknown"
    try:
      faces = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=True)
      if len (faces) >= 1:
        emotion = faces[0]['dominant_emotion']
        self.log.debug(f"Possible emotion: {emotion} for frame {id_frame} and face {id_face}.")
    except Exception as ex:
      self.log.warning(f"Não foi identificado um rosto ou expressão facial no frame {id_frame} : {ex}")
    return emotion

  def __get_face_box_positions__(self, frame: MatLike, detection) -> MatLike:
    height, width, _ = frame.shape
    box = detection.location_data.relative_bounding_box
    bbox = int(box.xmin * width), int(box.ymin * height), int(box.width * width), int(box.height * height)
    return bbox
