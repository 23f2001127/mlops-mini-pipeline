# MLOps Mini Pipeline

This project implements a reproducible mini-MLOps pipeline as part of an ML Engineering Internship technical assessment.

It demonstrates:
- Deterministic execution using config.yaml
- Rolling mean signal generation
- Structured metrics output (metrics.json)
- Logging (run.log)
- Docker containerization

---

## 📂 Files

- run.py – Main pipeline script  
- config.yaml – Configuration file  
- data.csv – Provided dataset  
- requirements.txt – Python dependencies  
- Dockerfile – Container setup  
- metrics.json – Example output  
- run.log – Example logs  

---

## ⚙️ Setup (Local)

Install dependencies:

pip install -r requirements.txt

Run the pipeline:

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

---

## 🐳 Docker

Build image:

docker build -t mlops-task .

Run container:

docker run --rm mlops-task

The container will generate:
- metrics.json
- run.log

and print metrics to terminal.

---

## 📊 Expected Output

metrics.json format:

```{
  "version": "v1",
  "rows_processed": 10000,
  "metric": "signal_rate",
  "value": 0.4990,
  "latency_ms": 127,
  "seed": 42,
  "status": "success"
}
```

---

## 📦 Dependencies

- pandas
- numpy
- pyyaml

---

## 🧠 Notes

This project demonstrates reproducibility, logging, and containerized batch ML pipelines.
