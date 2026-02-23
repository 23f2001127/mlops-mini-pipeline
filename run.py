import argparse
import yaml
import json
import time
import os
import sys
import logging
import pandas as pd
import numpy as np


def setup_logger(log_path):
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def write_error(output_path, version, message):
    err = {
        "version": version,
        "status": "error",
        "error_message": message,
    }
    with open(output_path, "w") as f:
        json.dump(err, f, indent=4)

    print(json.dumps(err, indent=2))  # required stdout
    logging.exception(message)


def load_config(config_path):
    if not os.path.exists(config_path):
        raise ValueError("Config file missing")

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except Exception:
        raise ValueError("Invalid YAML format")

    for key in ["seed", "window", "version"]:
        if key not in config:
            raise ValueError(f"Missing config key: {key}")

    if not isinstance(config["seed"], int):
        raise ValueError("Seed must be integer")

    if not isinstance(config["window"], int) or config["window"] <= 0:
        raise ValueError("Window must be positive integer")

    return config


def load_data(input_path):
    if not os.path.exists(input_path):
        raise ValueError("Input file missing")

    try:
        df = pd.read_csv(input_path)
    except Exception:
        raise ValueError("Invalid CSV format")

    if df.empty:
        raise ValueError("CSV file is empty")

    if "close" not in df.columns:
        raise ValueError("Missing 'close' column")

    # Ensure close is numeric
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    if df["close"].isna().all():
        raise ValueError("'close' column is not numeric")

    return df


def main(input_path, config_path, output_path, log_path):
    start_time = time.time()
    setup_logger(log_path)
    logging.info("Job started")

    version = "unknown"

    try:
        # ---- Load Config ----
        config = load_config(config_path)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)
        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        # ---- Load Data ----
        df = load_data(input_path)
        rows = len(df)
        logging.info(f"Data loaded: {rows} rows")

        # ---- Rolling Mean ----
        df["rolling_mean"] = df["close"].rolling(
            window=window,
            min_periods=window
        ).mean()
        logging.info(f"Rolling mean calculated with window={window}")

        # ---- Signal Generation ----
        df["signal"] = np.where(
            df["rolling_mean"].isna(),
            0,
            (df["close"] > df["rolling_mean"]).astype(int)
        )
        logging.info("Signals generated")

        signal_rate = round(float(df["signal"].mean()), 4)
        latency_ms = int((time.time() - start_time) * 1000)

        metrics = {
            "version": version,
            "rows_processed": rows,
            "metric": "signal_rate",
            "value": signal_rate,
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success",
        }

        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=4)

        print(json.dumps(metrics, indent=2))  # required stdout
        logging.info(f"Metrics: signal_rate={signal_rate}, rows_processed={rows}")
        logging.info(f"Job completed successfully in {latency_ms}ms")

    except Exception as e:
        write_error(output_path, version, str(e))
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini MLOps Pipeline")
    parser.add_argument("--input", required=True, help="Path to input CSV")
    parser.add_argument("--config", required=True, help="Path to config YAML")
    parser.add_argument("--output", required=True, help="Path to metrics JSON")
    parser.add_argument("--log-file", required=True, help="Path to log file")

    args = parser.parse_args()
    main(args.input, args.config, args.output, args.log_file)