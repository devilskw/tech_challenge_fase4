import logging
import os

from pos_ai_video_analyzer import MyRecognizer
from utils.json import JsonUtils


logging.basicConfig(level=logging.INFO)


config = JsonUtils.load_json("assets/config.json")

my_recognizer = MyRecognizer(config)
my_recognizer.analyze('teste.mp4')
