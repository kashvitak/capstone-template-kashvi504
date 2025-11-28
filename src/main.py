"""
Invention Assistant – Main entrypoint with CLI.

Usage:
    python src/main.py --title "My Invention" --description "..." [--debug]
    python src/main.py --input-file sample.json [--debug]

Outputs JSON + Markdown to `outputs/` folder.
"""
import argparse
import logging
import json
from datetime import datetime
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


def save_outputs(invention_title: str, result: dict) -> dict:
    """Save transcript + scorecard to JSON and Markdown files in outputs/ folder.
    
    Returns a dict with keys `json_path` and `markdown_path` pointing to saved files.
    """
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # sanitize title for filename
    safe_title = "".join(c if c.isalnum() else "_" for c in invention_title)[:30]
    
    json_file = output_dir / f"{timestamp}_{safe_title}.json"
    md_file = output_dir / f"{timestamp}_{safe_title}.md"
    
    # Save JSON
    with open(json_file, "w", encoding="utf8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    logging.info("Saved JSON to %s", json_file)
    
    # Generate and save Markdown
    md_content = _build_markdown_report(invention_title, result)
    with open(md_file, "w", encoding="utf8") as f:
        f.write(md_content)
    logging.info("Saved Markdown to %s", md_file)
    
    return {"json_path": str(json_file), "markdown_path": str(md_file)}


def _build_markdown_report(title: str, result: dict) -> str:
    """Build a readable Markdown report from result dict."""
    lines = [
        f"# Invention Assessment: {title}\n",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "\n## Analyst Transcript\n",
    ]
    
    # Add transcript entries
    transcript = result.get("transcript", [])
    for entry in transcript:
        role = entry.get("role", "Unknown")
        message = entry.get("message", "")
        lines.append(f"### {role}\n")
        lines.append(f"{message}\n")
    
    # Add scorecard
    lines.append("\n## Scorecard\n")
    scorecard = result.get("scorecard", {})
    
    for dim in ["technical_rigor", "originality", "feasibility", "impact"]:
        if dim in scorecard:
            item = scorecard[dim]
            score = item.get("score", 0)
            evidence = item.get("evidence", [])
            lines.append(f"### {dim.replace('_', ' ').title()}: {score}/5\n")
            if evidence:
                for ev in evidence:
                    lines.append(f"- {ev}\n")
            lines.append("")
    
    # Add overall decision
    overall = scorecard.get("overall", {})
    decision = overall.get("decision", "Unknown")
    rationale = overall.get("rationale", "")
    lines.append(f"\n## Overall Decision\n")
    lines.append(f"**Decision:** {decision.upper()}\n")
    lines.append(f"**Rationale:** {rationale}\n")
    
    return "\n".join(lines)


def run_experiment(invention: dict) -> dict:
    """Run the single Engineer persona analysis."""
    logging.info("Running experiment for invention: %s", invention.get("title"))
    try:
        # Use absolute import path to avoid relative import issues
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        from invention_assistant_graph import run_single_engineer
        result = run_single_engineer(invention)
    except Exception as e:
        logging.error("Failed to run engineer runner: %s", e)
        result = {
            "status": "error",
            "error": str(e),
            "transcript": [],
            "scorecard": {}
        }
    return result

def parse_args():
    parser = argparse.ArgumentParser(
        description="Run the Invention Assistant – evaluates inventions using LLM personas"
    )
    parser.add_argument("--title", default="", help="Invention title")
    parser.add_argument("--description", default="", help="Invention description")
    parser.add_argument("--input-file", default="", help="Path to JSON file with invention data (title, description keys)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging(args.debug)
    
    # Load invention data
    invention = {}
    if args.input_file:
        try:
            with open(args.input_file, "r", encoding="utf8") as f:
                invention = json.load(f)
            logging.info("Loaded invention from %s", args.input_file)
        except Exception as e:
            logging.error("Failed to load input file: %s", e)
            return
    else:
        invention = {
            "title": args.title or "Sample Invention",
            "description": args.description or "A lightweight personal air purifier using passive filters and a compact fan for wearable use."
        }
    
    # Run the experiment
    result = run_experiment(invention)
    
    # Save outputs
    outputs = save_outputs(invention.get("title", "invention"), result)
    logging.info("Results saved: JSON=%s, Markdown=%s", outputs["json_path"], outputs["markdown_path"])
    
    # Print summary to console
    logging.info("Experiment complete.")
    overall = result.get("scorecard", {}).get("overall", {})
    logging.info("Decision: %s", overall.get("decision", "Unknown"))
    if args.debug:
        import pprint
        pprint.pprint(result)


if __name__ == "__main__":
	main()

