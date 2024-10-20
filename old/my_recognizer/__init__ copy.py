from dataclasses import dataclass
import logging
from my_recognizer.gestures import MyRecognizerGestures
from utils.csv import CsvUtils
from utils.file import FileUtils
import cv2
import mediapipe.python.solutions.pose as mp_pose
from mediapipe.python.solutions.pose import Pose
import mediapipe.python.solutions.drawing_utils as PoseUtils
from tqdm import tqdm


@dataclass
class VideoProperties:
    width: int
    height: int
    fps: int
    total_frames: int
    codec: str


class MyRecognizer:
  in_basepath: str
  out_basepath: str
  video_extension: str
  log: logging.Logger
  cfg: dict

  def __init__(self, in_basepath, out_basepath, video_extension, my_recognizer_cgf: dict):
    self.in_basepath = in_basepath
    self.out_basepath = out_basepath
    self.video_extension = video_extension
    self.cfg = my_recognizer_cgf
    self.log = logging.getLogger(__name__)

  def recognize(self, video_filename: str):
    self.log.info('Inicializando a análise do vídeo com o My Recognizer.')

    self.log.debug('Inicializando a classe Pose do MediaPipe.')
    _pose = Pose()

    if ( self.cfg['webcam']):
      self.log.debug('Capturar vídeo em tempo real da webcam.')
      _cap = cv2.VideoCapture(0)
    else:
      self.log.debug(f"Capturar vídeo do arquivo {video_filename}.")
      _cap = cv2.VideoCapture(self.__get_full_file__(video_filename))

    self.log.debug('Verificando se o vídeo foi aberto corretamente.')
    if not _cap.isOpened():
      raise IOError(13, "Erro ao abrir o vídeo. O vídeo pode estar corrompido, inexistente, sem permissão ou ainda aberto por outra aplicação/ferramenta.")

    self.log.debug('Obtendo as propriedades do vídeo.')
    _prop = VideoProperties(
      width=int(_cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
      height=int(_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
      fps=_cap.get(cv2.CAP_PROP_FPS),
      total_frames=_cap.get(cv2.CAP_PROP_FRAME_COUNT),
      codec = int(_cap.get(cv2.CAP_PROP_FOURCC))
    )

    self.log.debug('Criando o objeto VideoWriter e iniciando a variavel id_frame para identificar cada frame.')
    id_frame = 0
    _out = cv2.VideoWriter(filename=self.out_basepath, fourcc=_prop.codec, fps=_prop.fps, frameSize=(_prop.width, _prop.height))

    self.log.debug('Loop para processar cada frame do vídeo e usando tqdm para criar a barra de progresso.')
    for _ in tqdm(range(_prop.total_frames), desc="Percentual de processamento do vídeo"):
      self.log.debug(f"Lendo o frame {id_frame} do vídeo.")
      id_frame += 1
      ret, frame = _cap.read()

      if not ret:
        self.log.warning(f"Não foi possível ler o frame {id_frame} do vídeo. Saindo...")
        break

      self.log.debug('Convertendo o frame para RGB e processando-o para detectar a pose.')
      rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      results = _pose.process(rgb_frame)

      if results.pose_landmarks:
        self.log.debug(f"Desenhando as anotações da pose no frame {id_frame}.")
        PoseUtils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if self.cfg['report']['enabled']:
          self.__gen_landmark_report_and_images__(video_filename, id_frame, frame, results.pose_landmarks.landmark)

        if self.cfg['gestures']['enabled']:
          self.__gen_gestures_report_and_images__(video_filename, id_frame, frame, results.pose_landmarks.landmark)

      self.log.debug('Escrevendo o frame processado com landmark no vídeo de saída.')
      _out.write(frame)

      self.log.debug('Exibir o frame processado.')
      cv2.imshow('Video', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        self.log.debug('Último o frame identificado.')
        break

    self.log.debug('Liberando a captura de vídeo e fechar todas as janelas em uso')
    _cap.release()
    _out.release()
    cv2.destroyAllWindows()


  def __gen_landmark_report_and_images__(self, video_filename, id_frame, frame, landmark):
    self.log.debug(f"Gerando print da imagem e anotando os dados do landmark do frame {id_frame}.")
    csv_file = self.__get_full_file__(f"{video_filename.replace('.mp4', '_landmarks_report.csv')}", False, self.cfg['report']['prefix'])
    img_file = self.__get_full_file__((video_filename.replace('.mp4', '')+ f"_landmarks_{id_frame}.png"), False, self.cfg['report']['prefix'])
    self.log.debug(f"Gerando imagem {img_file}.")
    cv2.imwrite(img_file, frame)
    self.log.debug(f"Atualizando relatorio {csv_file}.")
    _header = self.cfg['report']['header']
    _row = [id_frame, img_file]
    for i in range(0, 32, 1): # são 33 poses olhando o enum de PoseLandmark
      _row.append(landmark[i].x)
      _row.append(landmark[i].y)
      _row.append(landmark[i].z)
      _row.append(landmark[i].visibility)
    self.append_to_report(csv_file, _row, _header, id_frame == 1)

  def __gen_gestures_report_and_images__(self, video_filename, id_frame, frame, landmark):
    self.log.debug(f"Analisando gestosdo frame {id_frame}.")
    gestures = MyRecognizerGestures()
    gestures.analyze()

  def __get_full_file__(self, filename: str, from_input_path = True, prefix = ''):
    fullfile = self.in_basepath if from_input_path else self.out_basepath
    if prefix == '':
      fullfile = FileUtils.join(fullfile, prefix)
    return FileUtils.join(fullfile, filename)

  def append_to_report(self, csv_file: str, row: list, header: list=[], first_row = False):
    data = []
    if first_row and len(header) > 0:
        data.append(header)
    data.append(row)
    CsvUtils.save_csv(csv_file, data, first_row)

  def generate_frame_image(self, png_file: str, frame):
    cv2.imwrite(png_file, frame)