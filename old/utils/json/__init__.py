import json

class JsonUtils:
  @staticmethod
  def save_json(path, data, first_row = False):
    open_mode = 'w'
    if os.path.exists(path) and not first_row:
      open_mode = 'a+'

    with open(path, open_mode) as f:
      json.dump(data, f, ensure_ascii=False, indent=4)

  @staticmethod
  def load_json(path):
    with open(path) as f:
      return json.load(f)