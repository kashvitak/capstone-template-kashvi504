"""Test suite for schema validation of transcript and scorecard structures."""
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def validate_scorecard_schema(scorecard):
    """Validate that a scorecard has the required structure and types."""
    assert isinstance(scorecard, dict), "Scorecard must be a dict"
    
    # Check dimensions
    required_dims = ["technical_rigor", "originality", "feasibility", "impact"]
    for dim in required_dims:
        assert dim in scorecard, f"Missing dimension: {dim}"
        item = scorecard[dim]
        assert isinstance(item, dict), f"{dim} must be a dict"
        assert "score" in item, f"{dim} missing 'score'"
        assert "evidence" in item, f"{dim} missing 'evidence'"
        assert isinstance(item["score"], (int, float)), f"{dim} score must be numeric"
        assert 0 <= item["score"] <= 5, f"{dim} score must be 0-5"
        assert isinstance(item["evidence"], list), f"{dim} evidence must be a list"
    
    # Check overall
    assert "overall" in scorecard, "Missing 'overall' key"
    overall = scorecard["overall"]
    assert isinstance(overall, dict), "overall must be a dict"
    assert "decision" in overall, "overall missing 'decision'"
    assert "rationale" in overall, "overall missing 'rationale'"
    assert overall["decision"] in ["approve", "revise", "reject"], f"Invalid decision: {overall['decision']}"
    assert isinstance(overall["rationale"], str), "rationale must be a string"
    
    return True


def validate_transcript_schema(transcript):
    """Validate that a transcript is a list of properly structured entries."""
    assert isinstance(transcript, list), "Transcript must be a list"
    assert len(transcript) > 0, "Transcript must not be empty"
    
    for entry in transcript:
        assert isinstance(entry, dict), "Each transcript entry must be a dict"
        assert "role" in entry, "Missing 'role' in transcript entry"
        assert "message" in entry, "Missing 'message' in transcript entry"
        assert "citations" in entry, "Missing 'citations' in transcript entry"
        assert isinstance(entry["role"], str), "role must be a string"
        assert isinstance(entry["message"], str), "message must be a string"
        assert isinstance(entry["citations"], list), "citations must be a list"
    
    return True


def test_scorecard_schema_valid():
    """Test that a valid scorecard passes validation."""
    valid_scorecard = {
        "technical_rigor": {"score": 3.5, "evidence": ["point1", "point2"]},
        "originality": {"score": 4.0, "evidence": ["novel idea"]},
        "feasibility": {"score": 3.0, "evidence": ["feasible"]},
        "impact": {"score": 4.5, "evidence": ["high impact"]},
        "overall": {"decision": "approve", "rationale": "Good invention"}
    }
    assert validate_scorecard_schema(valid_scorecard)


def test_scorecard_schema_missing_dimension():
    """Test that missing dimension raises error."""
    invalid_scorecard = {
        "technical_rigor": {"score": 3.5, "evidence": []},
        "originality": {"score": 4.0, "evidence": []},
        # Missing feasibility
        "impact": {"score": 4.5, "evidence": []},
        "overall": {"decision": "approve", "rationale": "Good"}
    }
    try:
        validate_scorecard_schema(invalid_scorecard)
        assert False, "Should have raised error for missing dimension"
    except AssertionError as e:
        assert "Missing dimension" in str(e)


def test_scorecard_schema_invalid_score():
    """Test that score outside 0-5 raises error."""
    invalid_scorecard = {
        "technical_rigor": {"score": 10, "evidence": []},  # Invalid score
        "originality": {"score": 4.0, "evidence": []},
        "feasibility": {"score": 3.0, "evidence": []},
        "impact": {"score": 4.5, "evidence": []},
        "overall": {"decision": "approve", "rationale": "Good"}
    }
    try:
        validate_scorecard_schema(invalid_scorecard)
        assert False, "Should have raised error for invalid score"
    except AssertionError as e:
        assert "0-5" in str(e)


def test_scorecard_schema_invalid_decision():
    """Test that invalid decision raises error."""
    invalid_scorecard = {
        "technical_rigor": {"score": 3.5, "evidence": []},
        "originality": {"score": 4.0, "evidence": []},
        "feasibility": {"score": 3.0, "evidence": []},
        "impact": {"score": 4.5, "evidence": []},
        "overall": {"decision": "maybe", "rationale": "Good"}  # Invalid decision
    }
    try:
        validate_scorecard_schema(invalid_scorecard)
        assert False, "Should have raised error for invalid decision"
    except AssertionError as e:
        assert "Invalid decision" in str(e)


def test_transcript_schema_valid():
    """Test that a valid transcript passes validation."""
    valid_transcript = [
        {
            "role": "Engineer",
            "message": "This looks technically feasible.",
            "citations": ["ref1", "ref2"]
        },
        {
            "role": "Philosopher",
            "message": "Ethical considerations are important.",
            "citations": []
        }
    ]
    assert validate_transcript_schema(valid_transcript)


def test_transcript_schema_empty():
    """Test that empty transcript raises error."""
    invalid_transcript = []
    try:
        validate_transcript_schema(invalid_transcript)
        assert False, "Should have raised error for empty transcript"
    except AssertionError as e:
        assert "empty" in str(e).lower()


def test_transcript_schema_missing_field():
    """Test that missing field in transcript entry raises error."""
    invalid_transcript = [
        {
            "role": "Engineer",
            "message": "This looks feasible."
            # Missing 'citations'
        }
    ]
    try:
        validate_transcript_schema(invalid_transcript)
        assert False, "Should have raised error for missing field"
    except AssertionError as e:
        assert "citations" in str(e)


if __name__ == "__main__":
    # Run tests manually if pytest not available
    test_scorecard_schema_valid()
    test_scorecard_schema_missing_dimension()
    test_scorecard_schema_invalid_score()
    test_scorecard_schema_invalid_decision()
    test_transcript_schema_valid()
    test_transcript_schema_empty()
    test_transcript_schema_missing_field()
    print("✓ All schema tests passed!")
