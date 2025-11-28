"""Minimal single-analyst runner for the Invention Assistant MVP.

This module exposes `run_single_engineer(invention)` which accepts a dict with at least
`title` and `description` keys and returns a dict containing `transcript` and `scorecard`.

It uses `utils.llm_call` and `prompts.ENGINEER_PROMPT` to produce results. The wrapper
is intentionally simple so it is easy to replace with a LangGraph node later.
"""
from __future__ import annotations
import json
import logging
from typing import Any, Dict

try:
    from . import prompts, utils
except ImportError:
    # Fallback for direct execution (not as package)
    import prompts
    import utils


def build_engineer_prompt(invention: Dict[str, Any]) -> str:
    description = invention.get("description") or invention.get("title") or ""
    return prompts.ENGINEER_PROMPT.format(description=description)


def run_single_engineer(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single Engineer persona analysis.

    Returns:
      {"transcript": [...], "scorecard": {...}}
    """
    prompt = build_engineer_prompt(invention)
    logging.info("Calling LLM for Engineer persona")
    resp = utils.llm_call(prompt)

    # If the LLM returned raw text under `raw`, try to parse JSON from that text
    if isinstance(resp, dict) and "raw" in resp:
        text = resp["raw"]
        try:
            parsed = json.loads(text)
            return parsed
        except Exception:
            # fallback: wrap raw text in transcript
            return {
                "transcript": [{"role": "Engineer", "message": text, "citations": []}],
                "scorecard": {
                    "technical_rigor": {"score": 0, "evidence": []},
                    "originality": {"score": 0, "evidence": []},
                    "feasibility": {"score": 0, "evidence": []},
                    "impact": {"score": 0, "evidence": []},
                    "overall": {"decision": "revise", "rationale": "LLM returned non-JSON response"}
                }
            }

    # If response already looks like the desired dict, return it
    if isinstance(resp, dict) and ("transcript" in resp and "scorecard" in resp):
        return resp

    # Last-resort fallback: wrap whatever we have
    return {
        "transcript": [{"role": "Engineer", "message": str(resp), "citations": []}],
        "scorecard": {
            "technical_rigor": {"score": 0, "evidence": []},
            "originality": {"score": 0, "evidence": []},
            "feasibility": {"score": 0, "evidence": []},
            "impact": {"score": 0, "evidence": []},
            "overall": {"decision": "revise", "rationale": "Unexpected LLM response format"}
        }
    }
