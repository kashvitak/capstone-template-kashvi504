"""LangGraph implementation of the Invention Assistant.

This module uses LangGraph's StateGraph to orchestrate multiple analyst personas
in parallel, with proper state management and node definitions.
"""
from __future__ import annotations
import json
import logging
from typing import TypedDict, Annotated, List, Dict, Any
from operator import add

from langgraph.graph import StateGraph, END, START
from langchain_core.messages import BaseMessage

try:
    from . import prompts, utils
    from .rag import get_rag_system
    from .report_generator import generate_markdown_report
except ImportError:
    import prompts
    import utils
    from rag import get_rag_system
    from report_generator import generate_markdown_report


# Define the state schema
class InventionState(TypedDict):
    """State for the Invention Assistant graph."""
    invention: Dict[str, Any]  # Input invention description
    engineer_analysis: Dict[str, Any]  # Engineer's analysis
    philosopher_analysis: Dict[str, Any]  # Philosopher's analysis
    economist_analysis: Dict[str, Any]  # Economist's analysis
    visionary_analysis: Dict[str, Any]  # Visionary's analysis
    transcript: Annotated[List[Dict], add]  # Combined transcript (uses add reducer)
    aggregated_scorecard: Dict[str, Any]  # Final aggregated scorecard
    errors: Annotated[List[str], add]  # Any errors encountered
    feedback: str  # Feedback for refinement cycles


def build_prompt_for_persona(persona: str, invention: Dict[str, Any], use_rag: bool = True, feedback: str = "") -> str:
    """Build prompt for a specific persona with optional RAG context.
    
    Args:
        persona: Name of the analyst persona
        invention: Invention description dict
        use_rag: Whether to retrieve and include context from RAG
        feedback: Optional feedback from previous rounds (for cyclic refinement)
    """
    description = invention.get("description") or invention.get("title") or ""
    
    # Retrieve relevant context if RAG is enabled
    context = ""
    if use_rag:
        try:
            rag_system = get_rag_system()
            chunks = rag_system.retrieve_for_analyst(persona, description, k=3)
            if chunks:
                context = "\n\nRELEVANT DOMAIN KNOWLEDGE:\n" + "\n---\n".join(chunks)
                logging.info(f"Retrieved {len(chunks)} context chunks for {persona}")
        except Exception as e:
            logging.warning(f"RAG retrieval failed for {persona}: {e}")
    
    # Build the full prompt with context
    full_description = description + context
    
    # Append feedback if present
    if feedback:
        full_description += f"\n\nCRITICAL FEEDBACK FROM PREVIOUS ROUND: {feedback}\nPlease refine your analysis to address this feedback."
    
    if persona == "engineer":
        return prompts.ENGINEER_PROMPT.format(description=full_description)
    elif persona == "philosopher":
        return prompts.PHILOSOPHER_PROMPT.format(description=full_description)
    elif persona == "economist":
        return prompts.ECONOMIST_PROMPT.format(description=full_description)
    elif persona == "visionary":
        return prompts.VISIONARY_PROMPT.format(description=full_description)
    else:
        raise ValueError(f"Unknown persona: {persona}")


def parse_llm_response(resp: Any, persona: str) -> Dict[str, Any]:
    """Parse LLM response into standard format."""
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


# Node functions for each analyst
def engineer_node(state: InventionState) -> Dict[str, Any]:
    """Engineer analyst node."""
    try:
        logging.info("Engineer node: Analyzing invention")
        prompt = build_prompt_for_persona("engineer", state["invention"], feedback=state.get("feedback", ""))
        resp = utils.llm_call(prompt)
        analysis = parse_llm_response(resp, "engineer")
        
        return {
            "engineer_analysis": analysis,
            "transcript": analysis.get("transcript", [])
        }
    except Exception as e:
        logging.error(f"Error in engineer node: {e}")
        return {
            "engineer_analysis": {},
            "errors": [f"Engineer error: {str(e)}"]
        }


def philosopher_node(state: InventionState) -> Dict[str, Any]:
    """Philosopher analyst node."""
    try:
        logging.info("Philosopher node: Analyzing invention")
        prompt = build_prompt_for_persona("philosopher", state["invention"], feedback=state.get("feedback", ""))
        resp = utils.llm_call(prompt)
        analysis = parse_llm_response(resp, "philosopher")
        
        return {
            "philosopher_analysis": analysis,
            "transcript": analysis.get("transcript", [])
        }
    except Exception as e:
        logging.error(f"Error in philosopher node: {e}")
        return {
            "philosopher_analysis": {},
            "errors": [f"Philosopher error: {str(e)}"]
        }


def economist_node(state: InventionState) -> Dict[str, Any]:
    """Economist analyst node."""
    try:
        logging.info("Economist node: Analyzing invention")
        prompt = build_prompt_for_persona("economist", state["invention"], feedback=state.get("feedback", ""))
        resp = utils.llm_call(prompt)
        analysis = parse_llm_response(resp, "economist")
        
        return {
            "economist_analysis": analysis,
            "transcript": analysis.get("transcript", [])
        }
    except Exception as e:
        logging.error(f"Error in economist node: {e}")
        return {
            "economist_analysis": {},
            "errors": [f"Economist error: {str(e)}"]
        }


def visionary_node(state: InventionState) -> Dict[str, Any]:
    """Visionary analyst node."""
    try:
        logging.info("Visionary node: Analyzing invention")
        prompt = build_prompt_for_persona("visionary", state["invention"], feedback=state.get("feedback", ""))
        resp = utils.llm_call(prompt)
        analysis = parse_llm_response(resp, "visionary")
        
        return {
            "visionary_analysis": analysis,
            "transcript": analysis.get("transcript", [])
        }
    except Exception as e:
        logging.error(f"Error in visionary node: {e}")
        return {
            "visionary_analysis": {},
            "errors": [f"Visionary error: {str(e)}"]
        }


def aggregate_node(state: InventionState) -> Dict[str, Any]:
    """Aggregate all analyst scorecards into a final decision."""
    logging.info("Aggregate node: Combining all analyses")
    
    # Collect all analyses
    analyses = {
        "engineer": state.get("engineer_analysis", {}),
        "philosopher": state.get("philosopher_analysis", {}),
        "economist": state.get("economist_analysis", {}),
        "visionary": state.get("visionary_analysis", {})
    }
    
    # Aggregate scorecard dimensions
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
    
    return {
        "aggregated_scorecard": aggregated
    }


def refine_node(state: InventionState) -> Dict[str, Any]:
    """Generate feedback and prepare for refinement cycle."""
    logging.info("Refine node: Generating feedback for analysts")
    return {
        "feedback": "The previous analysis resulted in a REJECT decision. Please re-evaluate with a focus on mitigating the identified risks and improving feasibility."
    }


def check_quality(state: InventionState) -> str:
    """Check if the analysis quality is sufficient or needs refinement."""
    scorecard = state.get("aggregated_scorecard", {})
    overall = scorecard.get("overall", {})
    
    # If we already have feedback, it means we already refined once. Stop to avoid infinite loops.
    if state.get("feedback"):
        return "end"
        
    # If decision is 'reject', trigger refinement
    if overall.get("decision") == "reject":
        return "refine"
        
    return "end"


# Build the graph
def create_invention_graph() -> StateGraph:
    """Create the LangGraph StateGraph for invention analysis."""
    
    # Pre-initialize RAG system before building graph
    try:
        logging.info("Initializing RAG system for graph...")
        get_rag_system()
    except Exception as e:
        logging.warning(f"Could not initialize RAG system: {e}")
    
    # Create the graph
    workflow = StateGraph(InventionState)
    
    # Add nodes
    workflow.add_node("engineer", engineer_node)
    workflow.add_node("philosopher", philosopher_node)
    workflow.add_node("economist", economist_node)
    workflow.add_node("visionary", visionary_node)
    workflow.add_node("aggregate", aggregate_node)
    workflow.add_node("refine", refine_node)
    
    # Add edges - all analysts run in parallel from START
    workflow.add_edge(START, "engineer")
    workflow.add_edge(START, "philosopher")
    workflow.add_edge(START, "economist")
    workflow.add_edge(START, "visionary")
    
    # All analysts flow to aggregate
    workflow.add_edge("engineer", "aggregate")
    workflow.add_edge("philosopher", "aggregate")
    workflow.add_edge("economist", "aggregate")
    workflow.add_edge("visionary", "aggregate")
    
    # Aggregate flows to conditional check
    workflow.add_conditional_edges(
        "aggregate",
        check_quality,
        {
            "refine": "refine",
            "end": END
        }
    )
    
    # Refine node fans out to all analysts again
    workflow.add_edge("refine", "engineer")
    workflow.add_edge("refine", "philosopher")
    workflow.add_edge("refine", "economist")
    workflow.add_edge("refine", "visionary")
    
    # Compile with memory to support HITL (Human-in-the-loop)
    from langgraph.checkpoint.memory import MemorySaver
    
    # We use a simple in-memory checkpointer for this demo
    checkpointer = MemorySaver()
    
    # Compile the graph with an interrupt before aggregation
    return workflow.compile(
        checkpointer=checkpointer,
        interrupt_before=["aggregate"]
    )


# Expose the compiled graph for LangGraph Studio
graph = create_invention_graph()


# Compatibility wrapper for existing code
def run_all_analysts_parallel(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run invention analysis using LangGraph.
    
    This function replaces the old threading-based implementation with the new
    LangGraph-based one, while maintaining the same interface.
    """
    import uuid
    
    graph = create_invention_graph()
    
    # Initialize state
    initial_state: InventionState = {
        "invention": invention,
        "engineer_analysis": {},
        "philosopher_analysis": {},
        "economist_analysis": {},
        "visionary_analysis": {},
        "transcript": [],
        "aggregated_scorecard": {},
        "errors": []
    }
    
    # Create a unique thread ID for this run
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    logging.info(f"Starting graph execution with thread_id: {thread_id}")
    
    # Run the graph - it will pause before 'aggregate' due to interrupt_before
    # We use stream() to handle updates, but invoke() also works if we catch the pause
    # For simplicity in this wrapper, we'll just invoke it.
    
    # First run: Start -> Analysts -> Pause
    logging.info("Running analysts (Engineer, Philosopher, Economist, Visionary)...")
    graph.invoke(initial_state, config=config)
    
    # At this point, the graph is paused. 
    # In a real app, we would stop here and wait for user input.
    # For this demo function, we'll simulate "Human Approval" and continue.
    logging.info("Graph paused for human review. Resuming execution...")
    
    # Second run: Resume -> Aggregate -> End
    # We pass None as input to resume from the current state
    final_state = graph.invoke(None, config=config)
    
    # Format output to match expected structure
    return {
        "transcript": final_state.get("transcript", []),
        "scorecard": final_state.get("aggregated_scorecard", {}),
        "analyses": {
            "engineer": final_state.get("engineer_analysis", {}),
            "philosopher": final_state.get("philosopher_analysis", {}),
            "economist": final_state.get("economist_analysis", {}),
            "visionary": final_state.get("visionary_analysis", {})
        },
        "errors": final_state.get("errors", []) if final_state.get("errors") else None
    }


# Individual runners for compatibility/testing
def run_single_engineer(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single Engineer persona analysis (using node logic)."""
    state = {"invention": invention}
    result = engineer_node(state)
    return result["engineer_analysis"]

def run_single_philosopher(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single Philosopher persona analysis (using node logic)."""
    state = {"invention": invention}
    result = philosopher_node(state)
    return result["philosopher_analysis"]

def run_single_economist(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single Economist persona analysis (using node logic)."""
    state = {"invention": invention}
    result = economist_node(state)
    return result["economist_analysis"]

def run_single_visionary(invention: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single Visionary persona analysis (using node logic)."""
    state = {"invention": invention}
    result = visionary_node(state)
    return result["visionary_analysis"]
