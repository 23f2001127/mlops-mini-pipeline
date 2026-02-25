# MLOps Mini Pipeline

This project implements a reproducible mini-MLOps pipeline as part of an ML Engineering Internship technical assessment.

It demonstrates:
- Deterministic execution using config.yaml
- Rolling mean signal generation
- Structured metrics output (metrics.json)
- Detailed logging (run.log)
- Docker containerization for reproducibility

------------------------------------------------------------

## Files

- run.py – Main pipeline script  
- config.yaml – Configuration file  
- data.csv – Provided dataset  
- requirements.txt – Python dependencies  
- Dockerfile – Container setup  
- metrics.json – Example output  
- run.log – Example logs  

------------------------------------------------------------

## Setup (Local)

Install dependencies:

pip install -r requirements.txt

Run the pipeline:

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

------------------------------------------------------------

## Docker

Build image:

docker build -t mlops-task .

Run container:

docker run --rm mlops-task

The container will:
- Generate metrics.json
- Generate run.log
- Print metrics to terminal

------------------------------------------------------------

## Expected Output

Example metrics.json:

```
{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}
```

------------------------------------------------------------

## Dependencies

- pandas
- numpy
- pyyaml

------------------------------------------------------------

## Design Choices

Rolling Mean Signal  
A rolling mean of the close price is used as a simple deterministic baseline signal.  
Signal = 1 if close > rolling_mean, else 0.

Handling Initial Rows  
The first window-1 rows produce NaN rolling means. These rows are assigned signal = 0 to keep behavior deterministic.

Reproducibility  
All parameters (seed, window, version) are loaded from config.yaml.  
No hard-coded values are used.

Error Handling  
The pipeline validates:
- Missing input file  
- Invalid CSV format  
- Empty dataset  
- Missing close column  
- Invalid config  

Errors are written to metrics.json and run.log.

Dockerization  
Docker ensures consistent execution environment and reproducible runs across machines with a single command.

------------------------------------------------------------

## Notes

This project demonstrates core ML engineering practices:
- Config-driven pipelines
- Structured logging
- Deterministic runs
- Containerized deployment
- Machine-readable metrics