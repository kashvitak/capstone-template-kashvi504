"""Shared pytest fixtures and helpers for tests."""
import pytest
import json


@pytest.fixture
def sample_invention():
    """Sample invention for testing."""
    return {
        "title": "Smart Water Bottle",
        "description": "A water bottle with integrated sensors to track hydration levels and remind users to drink water.",
        "constraints": ["Battery life < 30 days", "Cost < $50"],
        "use_cases": ["Daily hydration tracking", "Sports hydration"],
        "assumptions": ["Users have smartphone", "WiFi connectivity available"]
    }


@pytest.fixture
def expected_scorecard_schema():
    """Expected structure for a scorecard result."""
    return {
        "technical_rigor": {"score": float, "evidence": list},
        "originality": {"score": float, "evidence": list},
        "feasibility": {"score": float, "evidence": list},
        "impact": {"score": float, "evidence": list},
        "overall": {"decision": str, "rationale": str}
    }


@pytest.fixture
def expected_transcript_schema():
    """Expected structure for transcript entries."""
    return {
        "role": str,
        "message": str,
        "citations": list
    }


@pytest.fixture
def mock_engineer_response():
    """Mock response from Engineer persona."""
    return {
        "transcript": [
            {
                "role": "Engineer",
                "message": "This smart water bottle is technically feasible. Key concerns: sensor accuracy, battery life, waterproofing.",
                "citations": []
            }
        ],
        "scorecard": {
            "technical_rigor": {"score": 3.5, "evidence": ["Proven sensor technology", "Integration challenges with mobile app"]},
            "originality": {"score": 3.0, "evidence": ["Similar products exist", "Novel sensor integration approach"]},
            "feasibility": {"score": 3.5, "evidence": ["Manufacturing is feasible", "Cost target achievable with scale"]},
            "impact": {"score": 3.0, "evidence": ["Useful for health-conscious users", "Market size moderate"]},
            "overall": {"decision": "revise", "rationale": "Strong technical foundation but needs market differentiation strategy."}
        }
    }
