"""main.py"""

from datetime import datetime
import sys
from pathlib import Path

from Point import Point
from DenStream import DenStream
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

spark = SparkSession.builder.appName("BigData").getOrCreate()
stream = StreamingContext(spark.sparkContext, 1)
input_stream = stream.textFileStream(sys.argv[1])
output_dir = Path(sys.argv[2])
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "outliers.txt"
ds = DenStream()
count = 0


def convert_line(raw_line: str):
    time, value = raw_line.split(",")
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    value = float(value)
    return Point(time, value)


def write_to_file(outlier_tuple):
    is_outlier, point = outlier_tuple
    with open(output_file, "a") as out_file:
        out_file.write(str(point.timestamp) + "," + str(point.value) + "\n")


def update_ds(rdd):
    converted_line = rdd.map(convert_line)
    outlier_check = converted_line.map(lambda point: (ds.merge(point.timestamp, point), point))
    outliers = outlier_check.filter(lambda outlier_tuple: not outlier_tuple[0])
    outliers.map(write_to_file).collect()


input_stream.foreachRDD(update_ds)

stream.start()
stream.awaitTermination()
spark.stop()
