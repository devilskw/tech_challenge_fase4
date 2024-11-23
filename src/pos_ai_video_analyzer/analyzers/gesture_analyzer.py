from cv2.typing import MatLike
import mediapipe.python.solutions.drawing_utils as mp_draw_utils
from mediapipe.python.solutions.pose import Pose
from mediapipe.python.solutions.pose import POSE_CONNECTIONS
from pos_ai_video_analyzer.analyzers import Analyzer
from pos_ai_video_analyzer.video_properties import VideoProperties
from pos_ai_video_analyzer.analyzers.gesture_rules.rules import GestureRuleResult
from pos_ai_video_analyzer.analyzers.gesture_rules import GestureRules

class GestureAnalyzer(Analyzer):

  gesture_rules = GestureRules
  def __init__(self, config: dict, video_property: VideoProperties):
    super().__init__(config, video_property)
    self.gesture_rules = GestureRules()

  def analyze(self, frame, id_frame, image):
    self.log.info(f"Analisando gestos do frame {id_frame} do vídeo.")
    with Pose(min_detection_confidence=self.cfg['min_detection_confidence']) as detection:
      result = detection.process(image)
      gestures = []
      landmks = []
      if result.pose_landmarks:
        self.log.debug(f"Encontrados possíveis gestos no frame {id_frame}.")
        for pose in [
          {"id":  0,"description":'NARIZ',"landmark":'NOSE'},
          {"id":  1,"description":'OLHO_ESQUERDO_INTERNO',"landmark":'LEFTEYEINNER'},
          {"id":  2,"description":'OLHO_ESQUERDO',"landmark":'LEFTEYE'},
          {"id":  3,"description":'OLHO_ESQUERDO_EXTERNO',"landmark":'LEFTEYEOUTER'},
          {"id":  4,"description":'OLHO_DIREITO_INTERNO',"landmark":'RIGHTEYEINNER'},
          {"id":  5,"description":'OLHO_DIREITO',"landmark":'RIGHTEYE'},
          {"id":  6,"description":'OLHO_DIREITO_EXTERNO',"landmark":'RIGHTEYEOUTER'},
          {"id":  7,"description":'ORELHA_ESQUERDA',"landmark":'LEFTEAR'},
          {"id":  8,"description":'ORELHA_DIREITA',"landmark":'RIGHTEAR'},
          {"id":  9,"description":'BOCA_ESQUERDA',"landmark":'MOUTHLEFT'},
          {"id": 10,"description":'BOCA_DIREITA',"landmark":'MOUTHRIGHT'},
          {"id": 11,"description":'OMBRO_ESQUERDO',"landmark":'LEFTSHOULDER'},
          {"id": 12,"description":'OMBRO_DIREITO',"landmark":'RIGHTSHOULDER'},
          {"id": 13,"description":'COTOVELO_ESQUERDO',"landmark":'LEFTELBOW'},
          {"id": 14,"description":'COTOVELO_DIREITO',"landmark":'RIGHTELBOW'},
          {"id": 15,"description":'PULSO_ESQUERDO',"landmark":'LEFTWRIST'},
          {"id": 16,"description":'PULSO_DIREITO',"landmark":'RIGHTWRIST'},
          {"id": 17,"description":'DEDO_MAO_MINDINHO_ESQUERDO',"landmark":'LEFTPINKY'},
          {"id": 18,"description":'DEDO_MAO_MINDINHO_DIREITO',"landmark":'RIGHTPINKY'},
          {"id": 19,"description":'DEDO_MAO_INDICADOR_ESQUERDO',"landmark":'LEFTINDEX'},
          {"id": 20,"description":'DEDO_MAO_INDICADOR_DIREITO',"landmark":'RIGHTINDEX'},
          {"id": 21,"description":'DEDO_MAO_POLEGAR_ESQUERDO',"landmark":'LEFTTHUMB'},
          {"id": 22,"description":'DEDO_MAO_POLEGAR_DIREITO',"landmark":'RIGHTTHUMB'},
          {"id": 23,"description":'QUADRIL_LADO_ESQUERDO',"landmark":'LEFTHIP'},
          {"id": 24,"description":'QUADRIL_LADO_DIREITO',"landmark":'RIGHTHIP'},
          {"id": 25,"description":'JOELHO_ESQUERDO',"landmark":'LEFTKNEE'},
          {"id": 26,"description":'JOELHO_DIREITO',"landmark":'RIGHTKNEE'},
          {"id": 27,"description":'TORNOZELO_ESQUERDO',"landmark":'LEFTANKLE'},
          {"id": 28,"description":'TORNOZELO_DIREITO',"landmark":'RIGHTANKLE'},
          {"id": 29,"description":'SALTO_ESQUERDO',"landmark":'LEFTHEEL'},
          {"id": 30,"description":'SALTO_DIREITO',"landmark":'RIGHTHEEL'},
          {"id": 31,"description":'DEDO_PE_INDICADOR_ESQUERDO',"landmark":'LEFTFOOTINDEX'},
          {"id": 32,"description":'DEDO_PE_INDICADOR_DIREITO',"landmark":'RIGHTFOOTINDEX'}
        ]:
          lndmk = result.pose_landmarks.landmark[pose['id']]
          landmks.append({
              'id_frame': id_frame
            , 'pose_id': pose['id']
            , 'pose': pose['landmark']
            , 'pose_ptbr': pose['description']
            , 'x': lndmk.x
            , 'y': lndmk.y
            , 'z': lndmk.z
            , 'visibility': lndmk.visibility
          })
        gestures = self.__identify_gestures__(id_frame, result.pose_landmarks.landmark)
        self.__draw_landmarks__(frame, id_frame, result.pose_landmarks, POSE_CONNECTIONS)
    return frame, gestures, landmks

  def __draw_landmarks__(self, frame: MatLike, id_frame, detections, conn: frozenset):
    self.log.debug(f"Desenhando landmark dos gestos {conn} no frame {id_frame}.")
    mp_draw_utils.draw_landmarks(frame, detections, conn)

  def __identify_gestures__(self, id_frame, lndmk):
    rules = self.gesture_rules.identify_gestures(lndmk)
    gestures = []
    for ix in range(len(rules)):
      gestures.append({
          'id_frame': id_frame
        , 'id_gesture': ix
        , 'gesture_name': rules[ix].name
        , 'gesture_description': rules[ix].description
      })
    return rules

