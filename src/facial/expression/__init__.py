from dataclasses import dataclass
import cv2
import logging
from DeepFace import DeepFace
from src.utils.csv import CsvUtils

#from tqdm import tqdm
# from fer import FER


@dataclass
class VideoProperties:
    width: int
    height: int
    fps: int
    total_frames: int

@dataclass
class FaceEmotionRow:
    id: int
    emotion: str
    posx_ini: int
    posx_end: int
    posy_ini: int
    posy_end: int
    img_path: str

class FaceDetector:

    in_basepath: str
    out_basepath: str
    video_extension: str
    log: logging.Logger
    codec: any

    def __init__(self, in_basepath: str, out_basepath: str, video_extension: str):
        self.in_basepath = in_basepath
        self.out_basepath = out_basepath
        self.video_extension = video_extension
        self.log = logging.getLogger(__name__)


    def detect(self, video_filename: str):
        self.log.info(f"Starting facial expression detection in {video_filename}... ")
        with cv2.VideoCapture(filename=f"{self.in_basepath}/{video_filename}") as cap:

            if not cap.isOpened():
                self.log.error(f"Erro ao abrir o arquivo {video_filename}")
                return

            _prop = VideoProperties(
                width=cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                height=cap.get(VideoProperties),
                fps=cap.get(VideoProperties),
                total_frames=cap.get(VideoProperties),
                codec = cv2.VideoWriter_fourcc(*f"{self.video_extension}")
            )
            _out = cv2.VideoWriter(self.out_basepath, _prop.codec, _prop.fps, (_prop.width, _prop.height))
            id_frame = 0

            while cap.isOpened():
                ret, frame = cap.read()
                id_frame += 1

                if not ret:
                    break

                self.__analyse_expressions__(frame, id_frame)
                _out.write(frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            _out.release()
            cv2.destroyAllWindows()
            return frame

    def __analyse_expressions__(self, frame, id_frame):
        try:
            faces = DeepFace.analyse(frame, actions=['emotion'], enforce_detection=False)
            id_face = 0
            for face in faces:
                id_face += 1
                img_file = f"{self.out_basepath}/video_frame_emotion_{id_frame}_{id_face}.png"
                csv_file = f"{self.out_basepath}/video_frame_emotion_analysis.csv"
                self.__add_frame_emotion_report__(face, id_face, img_file, csv_file)
                if id_frame < 4 and id_face < 20: # TODO SOMENTE PARA FINS DO TRABALHO (SE GERAR MUITAS IMAGENS A GENTE NÃO DEVE FAZER ISSO, OU RESTRINGIR PARA GERAR AS 'N' PRIMEIRAS IMAGENS SOMENTE, PARA VALIDAR)
                    self.__generate_image__(face, img_file)
        except Exception as ex: # TODO verificar e, se possível, especificar os tratamentos de exceção baseados nos erros possíveis
            # TODO verificar se vamos retornar o erro ou ignorar para proximo frame
            #
            # se for para ignorar:
            self.log.debug("Não foi identificado um rosto ou expressão facial no frame {id_frame} : {ex}")
            # se não for para ignorar:
            # self.log.error(f"Erro ao processar frame {id_frame}: {ex}")
            # raise ex

    def __generate_image__(self, face, img_file):
        # TODO VALIDAR SE ISSO FUNCIONARIA. A IDEIA SERIA TENTAR GERAR AS IMAGENS DAS EXPRESSOES FACIAIS DE FORMA ORGANIZADA
        # TODO SOMENTE PARA FINS DO TRABALHO (SE GERAR MUITAS IMAGENS A GENTE NÃO DEVE FAZER ISSO, OU RESTRINGIR PARA GERAR AS 'N' PRIMEIRAS IMAGENS SOMENTE, PARA VALIDAR)
        cv2.imwrite(img_file, face)

    def __add_frame_emotion_report__(self, face, id_face, img_file, csv_file):
        data = FaceEmotionRow(
            id_face,
            face['dominant_emotion'],
            face['region']['x'],
            face['region']['y'],
            face['region']['x'] + face['region']['w'],
            face['region']['y'] + face['region']['h'],
            img_file
        )
        CsvUtils.save_csv(csv_file, data)

