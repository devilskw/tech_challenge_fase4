import os
import logging
import cv2
from cv2.typing import MatLike
from tqdm import tqdm

from pos_ai_video_analyzer.analyzers.face_analyzer import FaceAnalyzer
from pos_ai_video_analyzer.analyzers.gesture_analyzer import GestureAnalyzer
from pos_ai_video_analyzer.video_properties import VideoProperties
from utils.csv import CsvUtils

class MyRecognizer:

  path_in: str
  path_out: str
  webcam: bool
  cfg: dict
  log: logging.Logger

  def __init__(self, config: dict):
    self.cfg = config
    self.path_in = config['path_in']
    self.path_out = config['path_out']
    self.webcam = config['webcam']
    self.log = logging.getLogger(__name__)

  def analyze(self, video_filename: str):
    _wait_key = 1 if self.webcam else 1
    _input = 0 if self.webcam else os.path.join(self.path_in, video_filename)
    id_frame = 0

    cap = cv2.VideoCapture(_input)

    if not cap.isOpened():
      raise IOError(13, "Erro ao tentar ler o video ou webcam. Verifique se não há outra aplicação/ferramenta acessando/usando, feche e tente novamente.")

    self.log.debug('Lendo as propriedades do video ou webcam.')
    _prop = VideoProperties(
      width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
      height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
      fps=int(cap.get(cv2.CAP_PROP_FPS)),
      total_frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
      codec = cv2.VideoWriter_fourcc(*'mp4v')
    )

    self.log.debug('Criando o objeto VideoWriter.')
    out = cv2.VideoWriter(filename=os.path.join(self.path_out, video_filename), fourcc=_prop.codec, fps=_prop.fps, frameSize=(_prop.width, _prop.height))

    self.log.debug('Iniciando a class de análise de rostos.')
    face_analyzer = FaceAnalyzer(self.cfg['analyzers']['face_analyzer'],  _prop)
    gesture_analyzer = GestureAnalyzer(self.cfg['analyzers']['gesture_analyzer'],  _prop)
    if self.webcam:
      while cap.isOpened():
        id_frame += 1
        ret, frame = self.__read_frame__(id_frame, cap)
        if not ret:
          self.log.warning(f"Não foi possível ler o frame {id_frame} do vídeo. Saindo...")
          break
        frame = self.__analyze_frame__(id_frame, frame, face_analyzer, gesture_analyzer, video_filename, True)
        out = self.__save_video__(out, frame)
        cv2.imshow("Teste webcam", frame)
        if cv2.waitKey(_wait_key) == 27 or cv2.getWindowProperty("Teste webcam", cv2.WND_PROP_VISIBLE) < 1: # esc key pressed == 27 ou fechar a janela
          break
    else:
      self.log.info(f"Total de frames que serão analisados: {_prop.total_frames}")
      for _ in tqdm(range(_prop.total_frames), desc="Percentual de processamento do vídeo"):
        id_frame += 1

        ret, frame = self.__read_frame__(id_frame, cap)
        if not ret:
          self.log.warning(f"Não foi possível ler o frame {id_frame} do vídeo. Saindo...")
          break

        if not self.cfg['test'] or (self.cfg['test'] and (id_frame % 50 == 0)):
          frame = self.__analyze_frame__(id_frame, frame, face_analyzer, gesture_analyzer, video_filename, False)

        out = self.__save_video__(out, frame)
        if cv2.waitKey(_wait_key) & 0xFF == ord('q'):
          break
    out.release()
    cap.release()
    cv2.destroyAllWindows()

  def __read_frame__(self, id_frame, cap: cv2.VideoCapture):
    self.log.debug(f"Lendo o frame {id_frame} do vídeo.")
    return cap.read()

  def __analyze_frame__(self, id_frame, frame: MatLike, face_analyzer: FaceAnalyzer, gesture_analyzer: GestureAnalyzer, video_filename, webcam: bool):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame, faces = face_analyzer.analyze(frame, id_frame, image)
    frame, gestures, landmks = gesture_analyzer.analyze(frame, id_frame, image)

    report_file = video_filename.replace(".mp4", ".csv")
    generate_validation_frame_image = 0
    generate_validation_frame_image += self.__append_faces_report__(report_file.replace(".csv", "_faces.csv"), id_frame, faces, first_row = id_frame == 1)
    self.__append_poses_report__(report_file.replace(".csv", "_poses_landmarks.csv"), id_frame, landmks, id_frame == 1)
    generate_validation_frame_image += self.__append_gestures_report__(report_file.replace(".csv", "_gestures.csv"), id_frame, gestures, id_frame == 1)

    if generate_validation_frame_image > 0:
      x = 10
      y= 30
      for gesture in gestures:
        cv2.putText(frame, gesture['gesture_description'],(x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        y+= 10
      x = 50
      y= 30
      for face in faces:
        cv2.putText(frame, face['emotion'],(x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    image_frame_file = video_filename.replace(".mp4", f"_{id_frame}.png")
    self.__save_video_image__(image_frame_file, frame)
    return frame

  def __append_faces_report__(self, filename, id_frame, faces, first_row = False):
    data = []
    header = ['id_frame', 'id_face', 'emotion', 'pos_x', 'pos_y', 'width', 'height']
    if (first_row):
      data.append(header)
    qtde_emotions = 0
    for face in faces:
      data.append([id_frame, face['id_face'], face['emotion'], face['pos_x'], face['pos_y'], face['width'], face['height']])
      if face['emotion'] != 'unknown': qtde_emotions += 1
    csv_file = os.path.join(self.path_out, filename)
    CsvUtils.save_csv(csv_file, data, first_row)
    return qtde_emotions

  def __append_poses_report__(self, filename, id_frame, gestures, first_row = False):
    data = []
    header = ['id_frame', 'pose_id', 'pose', 'pose_ptbr', 'pos_x', 'pos_y', 'visibility']
    if (first_row):
      data.append(header)
    for gesture in gestures:
      data.append([id_frame, gesture['pose_id'], gesture['pose'], gesture['pose_ptbr'], gesture['x'], gesture['y'], gesture['z'], gesture['visibility']])
    csv_file = os.path.join(self.path_out, filename)
    CsvUtils.save_csv(csv_file, data, first_row)

  def __append_gestures_report__(self, filename, id_frame, gestures, first_row = False):
    data = []
    header = ['id_frame', 'id_gesture', 'gesture_name', 'gesture_description']
    if (first_row):
      data.append(header)
    for gesture in gestures:
      data.append([id_frame, gesture['id_gesture'], gesture['gesture_name'], gesture['gesture_description']])
    csv_file = os.path.join(self.path_out, filename)
    CsvUtils.save_csv(csv_file, data, first_row)
    return len(gestures)

  def __save_video_image__(self, filename, frame):
    img_file = os.path.join(self.path_out, filename)
    cv2.imwrite(img_file, frame)

  def __save_video__(self, out: cv2.VideoWriter, frame: MatLike):
    self.log.debug('Escrevendo o frame processado com landmark no vídeo de saída.')
    out.write(frame)
    return out
