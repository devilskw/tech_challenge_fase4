from dataclasses import dataclass
import cv2
import logging
from utils.csv import CsvUtils
from deepface import DeepFace


@dataclass
class VideoProperties:
    width: int
    height: int
    fps: int
    total_frames: int
    codec: str

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
    codec: str

    def __init__(self, in_basepath: str, out_basepath: str, video_extension: str):
        self.in_basepath = in_basepath
        self.out_basepath = out_basepath
        self.video_extension = video_extension
        self.log = logging.getLogger(__name__)


    def detect(self, video_filename: str):
        self.log.info(f"Starting facial expression detection in {video_filename}... ")
        cap = cv2.VideoCapture(f"{self.in_basepath}\\{video_filename}")

        if not cap.isOpened():
            self.log.error(f"Erro ao abrir o arquivo {video_filename}")
            return
        
        print(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        _prop = VideoProperties(
            width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            fps=cap.get(cv2.CAP_PROP_FPS),
            total_frames=cap.get(cv2.CAP_PROP_FRAME_COUNT),
            codec = int(cap.get(cv2.CAP_PROP_FOURCC))
        )
        _out = cv2.VideoWriter(filename=self.out_basepath, fourcc=_prop.codec, fps=_prop.fps, frameSize=(_prop.width, _prop.height))
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
            faces = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            id_face = 0
            for face in faces:
                id_face += 1
                img_file = f"{self.out_basepath}/video_frame_emotion_{id_frame}_{id_face}.png"
                csv_file = f"{self.out_basepath}/video_frame_emotion_analysis.csv"
                self.__add_frame_emotion_report__(id_frame, id_face, face, img_file, csv_file, id_frame == 1)
                if id_frame % 25 == 0: # SOMENTE PARA FINS DO TRABALHO (SE GERAR MUITAS IMAGENS A GENTE NÃO DEVE FAZER ISSO, OU RESTRINGIR PARA GERAR AS 'N' PRIMEIRAS IMAGENS SOMENTE, PARA VALIDAR)
                    self.__generate_image__(face, frame, img_file)
        except Exception as ex:
            # ignorar e ir pro proximo frame:
            self.log.warning("Não foi identificado um rosto ou expressão facial no frame {id_frame} : {ex}")
            # se não for para ignorar:
            # self.log.error(f"Erro ao processar frame {id_frame}: {ex}")
            # raise ex

    def __generate_image__(self, face, frame, img_file):
        x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
        face_region = frame[y:y+h, x:x+w]
        cv2.imwrite(img_file, face_region)

    def __add_frame_emotion_report__(self, id_frame, id_face, face, img_file, csv_file, first_row = False):
        data = []
        if first_row:
            data.append(['id_frame', 'id_face','emotion','posx_ini','posy_ini','posx_end','posy_end','img_path'])
        data.append([id_frame, id_face, face['dominant_emotion'], face['region']['x'], face['region']['y'], face['region']['x'] + face['region']['w'], face['region']['y'] + face['region']['h'], img_file])
        CsvUtils.save_csv(csv_file, data, first_row)
