import os
import cv2
from cv2.typing import MatLike
from mediapipe.python.solutions.face_detection import FaceDetection
import mediapipe.python.solutions.drawing_utils as mp_draw_utils
from deepface import DeepFace

from pos_ai_video_analyzer.analyzers import Analyzer
from pos_ai_video_analyzer.video_properties import VideoProperties
from utils.csv import CsvUtils


class FaceAnalyzer(Analyzer):
  def __init__(self, config: dict, base_path_out: str, path_prefix: str, filename: str, video_property: VideoProperties):
    super().__init__(config, base_path_out, path_prefix, filename, video_property)

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
        # self.log.info("Vamos ver o face: ")
        # self.log.info(face)
        # img_file = os.path.join(self.path_out, f"{self.filename}_video_frame_emotion_{id_frame}_{id_face}.png")
        # bounding_box_image = self.__get_bounding_box_image__(frame, detection)
        # cv2.imwrite(img_file, bounding_box_image)
        # csv_file = os.path.join(self.path_out, f"{self.filename}_video_frame_emotion_analysis.csv")
        # self.__add_frame_emotion_report__(id_frame, id_face, face, img_file, csv_file, id_frame == 1)
    except Exception as ex:
      self.log.warning(f"Não foi identificado um rosto ou expressão facial no frame {id_frame} : {ex}")
    return emotion


  def __get_face_box_positions__(self, frame: MatLike, detection) -> MatLike:
    height, width, c = frame.shape
    box = detection.location_data.relative_bounding_box
    bbox = int(box.xmin * width), int(box.ymin * height), int(box.width * width), int(box.height * height)
    return bbox

  # def __get_bounding_box_image__(self, frame: MatLike, detection) -> MatLike:
  #   height, width, c = frame.shape
  #   box = detection.location_data.relative_bounding_box
  #   bbox = int(box.xmin * width), int(box.ymin * height), int(box.width * width), int(box.height * height)
  #   x, y, w, h = bbox
  #   bounding_face = frame[y:y+h, x:x+w]
  #   return bounding_face


  # def __add_frame_emotion_report__(self, id_frame, id_rosto, face, img_file, csv_file, first_row = False):
  #   data = []
  #   if first_row:
  #       data.append(['id_frame', 'id_rosto','emotion','posx_ini','posy_ini','posx_end','posy_end','img_path'])
  #   data.append([id_frame, id_rosto, face['dominant_emotion'], face['region']['x'], face['region']['y'], face['region']['x'] + face['region']['w'], face['region']['y'] + face['region']['h'], img_file])
  #   CsvUtils.save_csv(csv_file, data, first_row)

