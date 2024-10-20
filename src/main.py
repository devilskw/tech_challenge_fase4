import logging
import os

from pos_ai_video_analyzer import MyRecognizer
from utils.json import JsonUtils


logging.basicConfig(level=logging.INFO)


config = JsonUtils.load_json("assets/config.json")

my_recognizer = MyRecognizer(config)
my_recognizer.analyze('teste.mp4')


# Caminho para o vídeo de entrada e saída
# script_dir = os.path.dirname(os.path.abspath(__file__))
# input_video_path = os.path.join(config['general']['path_in'], config['video']['filename'])  # Nome do vídeo de entrada
# output_video_path = os.path.join(config['general']['path_out'], config['video']['filename'])  # Nome do vídeo de saída

# # Processar o vídeo
# detect_pose(config['general']['path_in'], config['general']['path_out'], config['video']['filename'])


# face_detector = FaceDetector(config['general']['path_in'], config['general']['path_out'], config['video']['extension'])
# face_detector.detect(config['video']['filename'])

 # análise de vídeo, através de técnicas de reconhecimento facial, análise de expressões emocionais em vídeos e detecção de atividades

# 1. Reconhecimento facial: Identifique e marque os rostos presentes no vídeo.
# 2. Análise de expressões emocionais: Analise as expressões emocionais dos rostos identificados.
# 3. Detecção de atividades: Detecte e categorize as atividades sendo realizadas no vídeo.
# 4. Geração de resumo: Crie um resumo automático das principais atividades e emoções detectadas no vídeo.