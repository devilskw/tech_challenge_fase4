import logging

from facial.expression import FaceDetector


path_in = "C:\\Users\\kazuo\\projetos\\ia\\FIAP\\fase4\\tech_challenge_fase4\\assets\\videos\\in"
path_out = "C:\\Users\\kazuo\\projetos\\ia\\FIAP\\fase4\\tech_challenge_fase4\\assets\\videos\\out"
face_detector = FaceDetector(path_in, path_out, ".mp4")

face_detector.detect("Unlocking Facial Recognition_ Diverse Activities Analysis.mp4")
