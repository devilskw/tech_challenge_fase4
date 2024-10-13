import csv
import os


class CsvUtils:

  @staticmethod
  def save_csv(path, data):
    open_mode = 'w'
    if os.path.exists(path):
      open_mode = 'a+'
    with open(path, open_mode, newline='') as f:
      csv_writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for row in data:
        csv_writer.writerow(row)