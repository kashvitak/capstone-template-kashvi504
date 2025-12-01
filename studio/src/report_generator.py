"""Report generator for the Invention Assistant.

This module formats the analysis results into a professional Markdown report.
"""
from typing import Dict, Any

def generate_markdown_report(result: Dict[str, Any]) -> str:
    """Generate a comprehensive Markdown report from the analysis result.
    
    Args:
        result: The output dictionary from the invention assistant graph.
        
    Returns:
        A formatted Markdown string.
    """
    transcript = result.get("transcript", [])
    scorecard = result.get("scorecard", {})
    analyses = result.get("analyses", {})
    
    # 1. Header
    report = "# Invention Analysis Report\n\n"
    
    # 2. Executive Summary
    overall = scorecard.get("overall", {})
    decision = overall.get("decision", "unknown").upper()
    rationale = overall.get("rationale", "No rationale provided.")
    
    decision_emoji = "✅" if decision == "APPROVE" else "⚠️" if decision == "REVISE" else "❌"
    
    report += f"## Executive Summary\n\n"
    report += f"**Final Decision:** {decision_emoji} {decision}\n\n"
    report += f"**Rationale:** {rationale}\n\n"
    
    # 3. Scorecard Summary Table
    report += "## Scorecard Summary\n\n"
    report += "| Dimension | Score (1-5) | Assessment |\n"
    report += "|---|---|---|\n"
    
    dims = ["technical_rigor", "originality", "feasibility", "impact"]
    for dim in dims:
        data = scorecard.get(dim, {})
        score = data.get("score", 0)
        # Create a visual bar for the score
        bar = "▓" * int(score) + "░" * (5 - int(score))
        report += f"| **{dim.replace('_', ' ').title()}** | {score}/5 {bar} | See details below |\n"
    report += "\n"
    
    # 4. Analyst Perspectives (Transcript)
    report += "## Analyst Perspectives\n\n"
    
    # Group transcript by role for cleaner reading
    for entry in transcript:
        role = entry.get("role", "Unknown")
        message = entry.get("message", "")
        citations = entry.get("citations", [])
        
        report += f"### 👤 {role}\n\n"
        report += f"{message}\n\n"
        
        if citations:
            report += "**Key References:**\n"
            for cite in citations:
                report += f"- *{cite}*\n"
            report += "\n"
            
    # 5. Detailed Evidence
    report += "## Detailed Evidence & Risks\n\n"
    
    for dim in dims:
        report += f"### {dim.replace('_', ' ').title()}\n"
        data = scorecard.get(dim, {})
        evidence = data.get("evidence", [])
        
        if evidence:
            for item in evidence:
                report += f"- {item}\n"
        else:
            report += "- No specific evidence cited.\n"
        report += "\n"
        
    return report
