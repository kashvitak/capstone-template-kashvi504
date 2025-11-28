"""
Starter entrypoint for running experiments as a normal Python script.

Usage:
	python src/main.py --data-path ../data --debug

This file provides a minimal structure: logging, argument parsing,
data-loading placeholder, and a `main()` function so you can expand
your project without notebooks.
"""
import argparse
import logging
import os
from pathlib import Path


def setup_logging(debug: bool = False) -> None:
	level = logging.DEBUG if debug else logging.INFO
	logging.basicConfig(
		level=level,
		format="%(asctime)s - %(levelname)s - %(message)s",
	)


def load_data(data_path: str):
	"""Placeholder for data-loading logic.

	Replace this with actual code to read CSVs, JSON, or other files
	from your `data/` directory.
	"""
	p = Path(data_path)
	logging.info("Looking for data in %s", p.resolve())
	if not p.exists():
		logging.warning("Data path does not exist: %s", p)
		return None
	# Example: list files
	files = list(p.rglob("*.*"))
	logging.info("Found %d files under %s", len(files), p)
	return files


def run_experiment(data_files, config: dict):
    """Run a minimal experiment: call the single Engineer persona runner.

    This function will: pick a single input (or a default sample), call the
    `run_single_engineer` runner, and return its structured result.
    """
    logging.info("Running experiment with %d data files", len(data_files) if data_files else 0)
    # Choose an input description. If no data files were found, use a small sample.
    sample_invention = {
        "title": "Prototype Invention",
        "description": "A lightweight personal air purifier using passive filters and a compact fan for wearable use."
    }
    invention = sample_invention
    # If you have actual data files, you could load one here instead.
    try:
        from invention_assistant_graph import run_single_engineer
        result = run_single_engineer(invention)
    except Exception as e:
        logging.warning("Failed to run engineer runner: %s", e)
        result = {"status": "error", "error": str(e)}
    return result

def parse_args():
	parser = argparse.ArgumentParser(description="Run experiments from script")
	parser.add_argument("--data-path", default="data", help="Path to data directory")
	parser.add_argument("--debug", action="store_true", help="Enable debug logging")
	return parser.parse_args()


def main():
	args = parse_args()
	setup_logging(args.debug)

	data_files = load_data(args.data_path)
	config = {"example_param": 1}
	result = run_experiment(data_files, config)
	logging.info("Experiment result: %s", result)


if __name__ == "__main__":
	main()

