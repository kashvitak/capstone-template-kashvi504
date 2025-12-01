"""Integration tests for the full Invention Assistant pipeline."""
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from test_schema import validate_scorecard_schema, validate_transcript_schema


def test_engineer_runner_with_mock():
    """Test that the engineer runner produces valid output (using mock)."""
    # Import after path is set
    from invention_assistant_graph import run_single_engineer
    
    invention = {
        "title": "Test Invention",
        "description": "A simple test invention for validation."
    }
    
    result = run_single_engineer(invention)
    
    # Check result structure
    assert isinstance(result, dict), "Result must be a dict"
    assert "transcript" in result, "Result missing 'transcript'"
    assert "scorecard" in result, "Result missing 'scorecard'"
    
    # Validate transcript
    validate_transcript_schema(result["transcript"])
    
    # Validate scorecard
    validate_scorecard_schema(result["scorecard"])
    
    print("✓ Engineer runner integration test passed!")


def test_sample_run_end_to_end():
    """Test a complete end-to-end run with sample invention."""
    from invention_assistant_graph import run_single_engineer
    
    sample_invention = {
        "title": "Biodegradable Phone Case",
        "description": "An eco-friendly phone case made from mushroom leather that degrades naturally after 5 years."
    }
    
    result = run_single_engineer(sample_invention)
    
    # Verify all required fields
    assert result["transcript"], "Transcript should not be empty"
    assert len(result["transcript"]) > 0, "Should have at least one analyst message"
    assert result["transcript"][0]["role"] == "Engineer", "First message should be from Engineer"
    
    # Verify scorecard completeness
    scorecard = result["scorecard"]
    assert scorecard["overall"]["decision"] in ["approve", "revise", "reject"], "Valid decision required"
    assert len(scorecard["overall"]["rationale"]) > 0, "Rationale should be provided"
    
    # Print sample output
    print("\n--- Sample Run Output ---")
    print(f"Invention: {sample_invention['title']}")
    print(f"Decision: {scorecard['overall']['decision'].upper()}")
    print(f"Rationale: {scorecard['overall']['rationale']}")
    print("Scores:")
    for dim in ["technical_rigor", "originality", "feasibility", "impact"]:
        score = scorecard[dim]["score"]
        print(f"  {dim.title()}: {score}/5")
    print("-" * 40)
    
    print("✓ End-to-end integration test passed!")


if __name__ == "__main__":
    # Run tests manually
    test_engineer_runner_with_mock()
    test_sample_run_end_to_end()
    print("\n✓ All integration tests passed!")
