import os
from typing import LiteralString

class FileUtils:
  @staticmethod
  def join_files(path, *paths) -> str:
    return os.path.join(path, paths)