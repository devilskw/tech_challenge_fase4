import logging
import os
from pose import detect_pose

logging.basicConfig(level=logging.INFO)

from facial.expression import FaceDetector
from utils.json import JsonUtils

config = JsonUtils.load_json("assets/config.json")

# Caminho para o vídeo de entrada e saída
script_dir = os.path.dirname(os.path.abspath(__file__))
input_video_path = os.path.join(config['general']['path_in'], config['video']['filename'])  # Nome do vídeo de entrada
output_video_path = os.path.join(config['general']['path_out'], config['video']['filename'])  # Nome do vídeo de saída

# Processar o vídeo
detect_pose(config['general']['path_in'], config['general']['path_out'], config['video']['filename'])


# face_detector = FaceDetector(config['general']['path_in'], config['general']['path_out'], config['video']['extension'])
# face_detector.detect(config['video']['filename'])