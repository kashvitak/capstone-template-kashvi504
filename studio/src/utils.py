"""Utility helpers: lightweight LLM wrapper (mock-first), JSON save/load, schema checks.

This wrapper will return deterministic mock outputs when no API key / SDK is available,
so you can develop offline. If `OPENAI_API_KEY` is set and `openai` package is installed,
it will attempt a real request (simple completion call). Replace or extend with your
preferred provider later.
"""
from __future__ import annotations
import json
import os
import logging
from pathlib import Path
from typing import Any, Dict

# Load .env file at module import
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, skip loading


def save_json(path: str, data: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf8") as f:
        return json.load(f)


def llm_call(prompt: str, max_tokens: int = 512) -> Dict[str, Any]:
    """Lightweight LLM call abstraction.

    Behavior:
    - If `OPENAI_API_KEY` is present and `openai` is installed, try a completion call.
    - Otherwise, return a deterministic mock response useful for local development/testing.

    The function returns a dict with at least `transcript` and `scorecard` keys.
    """
    # Try to call OpenAI if available
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            logging.info("Using OpenAI API for LLM call (this may incur cost)")
            # Use chat completion interface (gpt-3.5-turbo or gpt-4)
            resp = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert analyst. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.2,
            )
            text = resp.choices[0].message.content.strip()
            # Attempt to parse JSON from the response; fall back to raw text
            try:
                return json.loads(text)
            except Exception:
                return {"raw": text}
        except Exception as e:
            logging.warning("OpenAI call failed: %s — falling back to mock.", e)

    # Mock deterministic response for offline development
    logging.info("No LLM API available — returning mock response")
    mock = {
        "transcript": [
            {
                "role": "Engineer",
                "message": "This is a mock engineer assessment: concept seems plausible; main hazards are materials sourcing and regulatory compliance.",
                "citations": []
            }
        ],
        "scorecard": {
            "technical_rigor": {"score": 3.0, "evidence": ["Mock: basic technical assessment"]},
            "originality": {"score": 3.5, "evidence": ["Mock: some novel combination of ideas"]},
            "feasibility": {"score": 3.0, "evidence": ["Mock: feasible with moderate engineering effort"]},
            "impact": {"score": 3.5, "evidence": ["Mock: positive social impact potential"]},
            "overall": {"decision": "revise", "rationale": "Mock: proceed with experimental prototype and risk mitigation"}
        }
    }
    return mock
