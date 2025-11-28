# Architecture – Invention Assistant (MAT496 Capstone)

A transcript‑driven, multi‑analyst evaluator built on LangGraph.  
This document defines goals, modules, state, data flow, schemas, and operational details so the system is reproducible and viva‑ready.

---

## System Goals and Requirements

- **Primary Goal:** Evaluate invention ideas via a panel of specialized analyst personas, producing a structured scorecard and narrative transcript.
- **Core Capabilities:** Ingest unstructured text, enrich with retrieval, orchestrate persona analysis, aggregate structured outputs, and present a concise decision summary.
- **Coverage of Course Topics:** Prompting, Structured Output, Semantic Search, RAG, Tool Calling, LangGraph (state + nodes + graph), LangSmith debugging.
- **Quality Attributes:**  
  - Reliability: deterministic graph orchestration with explicit state transitions.  
  - Traceability: full run traces, persona prompts, and scorecards logged.  
  - Reproducibility: fixed schemas, versioned prompts, seeded demo inputs.  
  - Performance: retrieval batching, parallel persona execution.

---

## High‑Level Architecture

- **User Interface Layer:** CLI or notebook interface to accept invention descriptions.  
- **LangGraph Orchestration Layer:** Graph controlling state and node execution.  
- **Knowledge + Tools Layer:** Semantic search, RAG, hazard table generator, feasibility chart generator.  
- **Persistence + Observability:** Logs, transcripts, scorecards; LangSmith for debugging.

---

## Data Flow and State Model

### State Shape

```json
{
  "input": {
    "title": "string",
    "description": "string",
    "constraints": ["string"],
    "use_cases": ["string"],
    "assumptions": ["string"]
  },
  "retrieval": {
    "queries": ["string"],
    "contexts": [
      {"source": "string", "content": "string", "relevance": "number"}
    ]
  },
  "analysis": {
    "engineer": {"findings": [], "risks": [], "tables": []},
    "philosopher": {"themes": [], "ethical_considerations": [], "historical_refs": []},
    "economist": {"market": [], "costs": [], "adoption_curve": []},
    "visionary": {"scenarios": [], "narratives": [], "long_term_implications": []}
  },
  "transcript": [
    {"role": "string", "message": "string", "citations": ["sourceId"]}
  ],
  "scorecard": {
    "technical_rigor": {"score": 0, "evidence": []},
    "originality": {"score": 0, "evidence": []},
    "feasibility": {"score": 0, "evidence": []},
    "impact": {"score": 0, "evidence": []},
    "overall": {"decision": "approve|revise|reject", "rationale": "string"}
  }
}

User → Input Parser → Retrieval Planner → Retriever → Evidence Normalizer
     → Parallel Analyst Nodes (Engineer, Philosopher, Economist, Visionary)
     → Transcript Weaver → Scorecard Aggregator → Presenter

Components and Nodes
Input Parser Node: Normalize user input into structured fields.

Retrieval Planner Node: Generate queries across technical, ethical, market, visionary domains.

Retriever Node (RAG): Semantic search, top‑k selection, snippet compression.

Evidence Normalizer Node: Deduplicate, rank, and label sources with IDs.

Engineer Node: Assess hazards, dependencies, feasibility; output hazard tables.

Philosopher Node: Ethical analysis, conceptual framing, historical parallels.

Economist Node: Market sizing, cost structure, adoption dynamics.

Visionary Node: Scenario building, narratives, long‑term implications.

Transcript Weaver Node: Compose analyst messages into panel dialogue.

Scorecard Aggregator Node: Compute rubric scores and overall decision.

Presenter Node: Package transcript + scorecard into Markdown + JSON.


{"role":"Engineer|Philosopher|Economist|Visionary","message":"string","citations":["sourceId"]}


{
  "technical_rigor":{"score":0,"evidence":["string"]},
  "originality":{"score":0,"evidence":["string"]},
  "feasibility":{"score":0,"evidence":["string"]},
  "impact":{"score":0,"evidence":["string"]},
  "overall":{"decision":"approve|revise|reject","rationale":"string"}
}

Persona Prompting Strategy
Engineer: Assess feasibility, hazards, dependencies; produce hazard table.

Philosopher: Highlight ethical tensions, conceptual frames, historical analogues.

Economist: Estimate market size, costs, adoption curve; flag risks.

Visionary: Compose plausible future scenarios; highlight opportunities and risks.

Scoring Rubric
Technical Rigor (30%) → hazards, dependencies, mitigations.

Originality (20%) → novelty, distinct scenario framing.

Feasibility (25%) → realism, adoption plausibility, blockers.

Impact (25%) → social/ethical value, breadth of use cases.

Decision Rule: Weighted average ≥ 3.5 → approve; critical blocker → revise.

Operations and Deliverables
Run Modes:

Demo mode → seeded examples, fixed corpus.

Live mode → dynamic retrieval, logs persisted.

Observability: LangSmith traces, prompt regression tests.

Testing: Unit tests for schema, integration tests for pipeline runs.

Deliverables:

docs/architecture.md (this file)

README.md (project plan + conclusion)

Demo transcripts + scorecards

Commit history with [TODO] → [DONE] transitions

[Input Parser]
      |
      v
[Retrieval Planner] → [Retriever] → [Evidence Normalizer]
      |
      v
   (state) → [Engineer] [Philosopher] [Economist] [Visionary]
      |               |               |               |
      v               v               v               v
      ----------------→ [Transcript Weaver] → [Scorecard Aggregator] → [Presenter]



---

✨ This file is structured exactly how professors expect: clear goals, nodes, state, schemas, prompts, scoring, and deliverables.  

Would you like me to also **generate a starter `graph.py` scaffold** that matches this architecture, so you can commit Step 2 right away in your repo?