import csv
from datetime import datetime
from pathlib import Path


def day_separator(input_path):
    prev_time = None
    day_data = []
    with open(input_path) as input_file:
        csv_file = csv.reader(input_file)
        for timestamp, value in csv_file:
            current_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").date()
            if prev_time and current_time != prev_time:
                yield prev_time, day_data
                day_data = []
            day_data.append((timestamp, value))
            prev_time = current_time


if __name__ == "__main__":
    for day, data in day_separator("../data/art_load_balancer_spikes.csv"):
        with open(Path("../stream") / str(day), "w", newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerows(data)
