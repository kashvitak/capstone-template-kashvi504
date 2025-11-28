"""Minimal single-analyst runner for the Invention Assistant MVP.

This module exposes `run_single_engineer(invention)` which accepts a dict with at least
`title` and `description` keys and returns a dict containing `transcript` and `scorecard`.

It uses `utils.llm_call` and `prompts.ENGINEER_PROMPT` to produce results. The wrapper
is intentionally simple so it is easy to replace with a LangGraph node later.
"""
from __future__ import annotations
import json
import logging
import threading
from typing import Any, Dict

try:
    from . import prompts, utils
except ImportError:
    # Fallback for direct execution (not as package)
    import prompts
    import utils


def build_prompt_for_persona(persona: str, invention: Dict[str, Any]) -> str:
    """Build prompt for a specific persona."""
    description = invention.get("description") or invention.get("title") or ""
    
    if persona == "engineer":
        return prompts.ENGINEER_PROMPT.format(description=description)
    elif persona == "philosopher":
        return prompts.PHILOSOPHER_PROMPT.format(description=description)
    elif persona == "economist":
        return prompts.ECONOMIST_PROMPT.format(description=description)
    elif persona == "visionary":
        return prompts.VISIONARY_PROMPT.format(description=description)
    else:
        raise ValueError(f"Unknown persona: {persona}")


def _run_single_analyst(persona: str, invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single analyst (internal helper)."""
    prompt = build_prompt_for_persona(persona, invention)
    logging.info("Calling LLM for %s persona", persona.title())
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
                "transcript": [{"role": persona.title(), "message": text, "citations": []}],
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
        "transcript": [{"role": persona.title(), "message": str(resp), "citations": []}],
        "scorecard": {
            "technical_rigor": {"score": 0, "evidence": []},
            "originality": {"score": 0, "evidence": []},
            "feasibility": {"score": 0, "evidence": []},
            "impact": {"score": 0, "evidence": []},
            "overall": {"decision": "revise", "rationale": "Unexpected LLM response format"}
        }
    }


def run_single_engineer(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single Engineer persona analysis."""
    return _run_single_analyst("engineer", invention)


def run_single_philosopher(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single Philosopher persona analysis."""
    return _run_single_analyst("philosopher", invention)


def run_single_economist(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single Economist persona analysis."""
    return _run_single_analyst("economist", invention)


def run_single_visionary(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single Visionary persona analysis."""
    return _run_single_analyst("visionary", invention)


def run_all_analysts_parallel(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run all four analysts in parallel and aggregate results.
    
    Returns:
      {
        "transcript": [...],  # combined from all analysts
        "scorecard": {        # aggregated scores + decisions
          "technical_rigor": {...},
          "originality": {...},
          "feasibility": {...},
          "impact": {...},
          "overall": {...}
        },
        "analyses": {         # individual analyses by persona
          "engineer": {...},
          "philosopher": {...},
          "economist": {...},
          "visionary": {...}
        }
      }
    """
    results = {}
    errors = {}
    
    # Define runner functions for each persona
    runners = {
        "engineer": run_single_engineer,
        "philosopher": run_single_philosopher,
        "economist": run_single_economist,
        "visionary": run_single_visionary
    }
    
    # Run each analyst in a thread
    threads = []
    for persona_name, runner_func in runners.items():
        def run_and_store(name, func):
            try:
                results[name] = func(invention)
            except Exception as e:
                logging.error("Error running %s: %s", name, e)
                errors[name] = str(e)
        
        thread = threading.Thread(target=run_and_store, args=(persona_name, runner_func))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Aggregate transcript (combine all analyst messages)
    combined_transcript = []
    for persona_name in ["engineer", "philosopher", "economist", "visionary"]:
        if persona_name in results:
            persona_result = results[persona_name]
            if "transcript" in persona_result:
                combined_transcript.extend(persona_result["transcript"])
    
    # Aggregate scorecard (average across personas)
    aggregated_scorecard = _aggregate_scorecards(results)
    
    return {
        "transcript": combined_transcript,
        "scorecard": aggregated_scorecard,
        "analyses": results,
        "errors": errors if errors else None
    }


def _aggregate_scorecards(analyses: Dict[str, Dict]) -> Dict[str, Any]:
    """Aggregate individual scorecards into a single scorecard.
    
    Averages scores across personas and produces an overall decision.
    """
    dims = ["technical_rigor", "originality", "feasibility", "impact"]
    aggregated = {}
    
    for dim in dims:
        scores = []
        all_evidence = []
        for persona_name, analysis in analyses.items():
            if "scorecard" in analysis and dim in analysis["scorecard"]:
                item = analysis["scorecard"][dim]
                if "score" in item:
                    scores.append(item["score"])
                if "evidence" in item:
                    all_evidence.extend(item["evidence"])
        
        avg_score = sum(scores) / len(scores) if scores else 0
        aggregated[dim] = {
            "score": round(avg_score, 1),
            "evidence": all_evidence[:3]  # top 3 pieces of evidence
        }
    
    # Compute overall decision based on average score
    overall_avg = sum(aggregated[d]["score"] for d in dims) / len(dims)
    
    if overall_avg >= 3.5:
        decision = "approve"
        rationale = "Overall strong evaluation across analysts. Proceed with development."
    elif overall_avg >= 2.5:
        decision = "revise"
        rationale = "Mixed evaluation. Address concerns raised by analysts before proceeding."
    else:
        decision = "reject"
        rationale = "Significant concerns identified. Fundamental rethinking recommended."
    
    aggregated["overall"] = {
        "decision": decision,
        "rationale": rationale
    }
    
    return aggregated
