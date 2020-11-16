# Unsupervised Real-Time Anomaly Detection for Streaming Data

## Algorithm
DenStream

Literature: https://archive.siam.org/meetings/sdm06/proceedings/030caof.pdf

## Run Instructions
On windows, you can use ```pip install --user pipenv``` to install pipenv
1. [Install](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) [pipenv](https://pipenv.pypa.io/en/latest/)
1. ```pipenv install```
1. ```pipenv shell```
1. ```python main.py```

In a separate terminal, run
```
cd scripts
./stream.sh
```

If you want to view the outliers file updating in real-time, run
```
tail -f output/
```

## Requirements
* Python **3.6**
* Spark 3.0
* Amazon EMR 6.1.0
