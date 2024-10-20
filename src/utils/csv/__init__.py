import csv
import os


class CsvUtils:

  @staticmethod
  def save_csv(path, data, first_row):
    open_mode = 'w'
    if os.path.exists(path) and not first_row:
      open_mode = 'a+'
    with open(path, open_mode, newline='') as f:
      csv_writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
      for row in data:
        csv_writer.writerow(row)
