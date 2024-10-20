import logging

logging.basicConfig(level=logging.INFO)

from facial.expression import FaceDetector
from utils.json import JsonUtils

config = JsonUtils.load_json("assets/config.json")

face_detector = FaceDetector(config['general']['path_in'], config['general']['path_out'], config['video']['extension'])
face_detector.detect(config['video']['filename'])