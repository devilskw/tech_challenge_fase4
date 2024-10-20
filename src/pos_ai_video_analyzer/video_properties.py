from dataclasses import dataclass
@dataclass
class VideoProperties:
    width: int
    height: int
    fps: int
    total_frames: int
    codec: str
