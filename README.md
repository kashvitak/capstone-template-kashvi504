Template for creating and submitting MAT496 capstone project.

# Overview of MAT496

In this course, we have primarily learned Langgraph. This is helpful tool to build apps which can process unstructured `text`, find information we are looking for, and present the format we choose. Some specific topics we have covered are:

- Prompting
- Structured Output 
- Semantic Search
- Retreaval Augmented Generation (RAG)
- Tool calling LLMs & MCP
- Langgraph: State, Nodes, Graph

We also learned that Langsmith is a nice tool for debugging Langgraph codes.

------

# Capstone Project objective

The first purpose of the capstone project is to give a chance to revise all the major above listed topics. The second purpose of the capstone is to show your creativity. Think about all the problems which you can not have solved earlier, but are not possible to solve with the concepts learned in this course. For example, We can use LLM to analyse all kinds of news: sports news, financial news, political news. Another example, we can use LLMs to build a legal assistant. Pretty much anything which requires lots of reading, can be outsourced to LLMs. Let your imagination run free.


-------------------------

# Project report Template

## Title: Invention Assistant - AI-Powered Product Evaluation Committee

## Overview

The **Invention Assistant** is an intelligent, multi-agent system designed to evaluate new product ideas, inventions, and startup concepts. It simulates a rigorous review committee by employing four distinct AI personas—an **Engineer**, a **Philosopher**, an **Economist**, and a **Visionary**—who analyze the invention in parallel.

Instead of a simple "good/bad" judgment, the system provides a comprehensive 360-degree analysis. It uses **Retrieval Augmented Generation (RAG)** to ground its evaluations in real-world knowledge (technical papers, market reports, ethical guidelines). The system aggregates these diverse perspectives into a unified scorecard and makes a final decision: **Approve**, **Revise**, or **Reject**.

Crucially, the system features a **self-correcting feedback loop**. If an invention is rejected (or receives a low score), the graph doesn't just stop; it generates specific, constructive feedback and routes the invention back to the analysts for a second round of refinement, simulating an iterative design review process.

## Reason for picking up this project

This project is a comprehensive implementation of the core concepts learned in MAT496, demonstrating:

- **LangGraph (Graph, Nodes, Edges)**: The core architecture is built on a `StateGraph` where **Nodes** represent analysts (Engineer, Philosopher, etc.) and **Edges** define the flow of execution.
- **Retrieval Augmented Generation (RAG)**: Each analyst node uses RAG to ground its analysis in real-world data, preventing hallucinations.
- **Semantic Search**: The RAG pipeline utilizes vector embeddings and semantic search to retrieve the most relevant documents for each specific invention context.
- **Human-in-the-Loop**: The graph is configured with an **interrupt** (`interrupt_before=["aggregate"]`) in LangGraph Studio. This allows a human user to pause execution, inspect the analysts' outputs, and potentially modify the state before the final decision is made.
- **Multi-Agent Collaboration**: Four distinct AI personas work in parallel, simulating a real-world committee.
- **State Management**: Complex state is maintained across the graph, tracking the invention, multiple analyses, transcripts, and scorecards.
- **Conditional Routing & Cycles**: The graph intelligently routes to a "Refine" node if quality is low, creating a feedback cycle—a key pattern in agentic workflows.

## Plan

I plan to excecute these steps to complete my project.
[DONE] Step 1: Set up project structure and environment
- Fork the MAT496 repository and create a new project folder for the Invention Assistant.
- Add a basic folder structure: src/, data/, docs/, notebooks/.
- Create an empty main Python file for the LangGraph app (e.g., src/invention_assistant_graph.py).
- Install minimal dependencies (langgraph, langchain, faiss-cpu, requests).

[DONE] Step 2: Implement basic LangGraph with a single analyst (no RAG)
- Define the LangGraph state (invention_description, contexts, analyses, transcript, scorecard).
- Implement a single node that acts as one analyst (Engineer persona) with a system prompt only.
- Build a minimal StateGraph with START → Engineer node → Scorecard node → END.
- Add a simple CLI/runner function to take user input and print a basic evaluation.
- Added comprehensive CLI with file I/O, JSON + Markdown output persistence.
- Integrated OpenAI API (mock fallback for offline dev).
- Created test suite: schema validation + integration tests.

[DONE] Step 3: Test and refine the single‑analyst flow
- Ran Engineer analyst on 3+ sample inventions (Smart Water Bottle, AI Classroom Assistant, Biodegradable Phone Case).
- Refined all 4 persona prompts with explicit guidance for hazards, dependencies, unknowns, and recommendations.
- Updated ENGINEER_PROMPT to emphasize: Hazards (electrical, mechanical, safety risks), Dependencies (prerequisites, infrastructure), Key Unknowns (technical uncertainties), Recommendation (single clear action).
- Similarly structured PHILOSOPHER_PROMPT (ethical framework), ECONOMIST_PROMPT (market analysis), VISIONARY_PROMPT (futures scenarios).
- Verified schema tests (7/7 passing) and integration tests (2/2 passing).
- Confirmed state structure consistency: all runs produce transcript + scorecard with 5 scorecard dimensions (technical_rigor, originality, feasibility, impact, overall).
- Verified evidence collection and decision consistency (approve/revise/reject decisions properly generated).

[DONE] Step 4: Extend the graph to use all four analysts (Engineer, Philosopher, Economist, Visionary)
- Add separate persona prompts for each analyst.
- Create individual nodes (or a shared node function) for each persona's analysis.
- Modify the graph to run all four analyses and store them in the state.
- Implement a scorecard node that combines all analyses into one unified evaluation.
- Parallel execution using threading for efficiency.
- Aggregated scoring (averaged across personas).
- Full transcript combining all analyst perspectives.

[DONE] Step 5: Collect raw reference content for each analyst domain
- Identify and list data sources (technical papers, ethics essays, market reports, foresight studies).
- Download or copy text content into the project’s data/ folder (separate subfolders per analyst).
- Normalize the content into plain text files ready for preprocessing.

[DONE] Step 6: Preprocess and chunk the reference content
- Write a preprocessing script to clean and chunk the raw text (remove formatting noise).
- Split content into semantically meaningful chunks suitable for retrieval.
- Save the processed chunks in a structured format (e.g., JSON or plain text per analyst).

[DONE] Step 7: Build a simple RAG pipeline for each analyst
- Create embeddings for the processed chunks using an embedding model.
- Store the embeddings in a vector store (e.g., FAISS).
- Implement a retrieval function that, given an analyst and a query, returns the top‑k relevant chunks.
- Test retrieval independently with a few example queries.

[DONE] Step 8: Integrate RAG into the LangGraph nodes
- Update each analyst node to call the retrieval function and include retrieved chunks in the prompt.
- Ensure the analysis combines:
(a) the user’s invention description, and
(b) domain knowledge retrieved from that analyst’s data.
- Verify that the state correctly stores enriched analyses using RAG‑enabled responses.

[DONE] Step 9: Polish the transcript and scorecard structure
- Design a clear, structured transcript format (dialogue style with citations).
- Update the scorecard node prompt to always follow rubric dimensions (Technical Rigor, Originality, Feasibility, Impact).
- Add section headings and bullet points so the output looks like a professional evaluation report.

[DONE] Step 10: Create sample scenarios and test the full pipeline
- Prepare multiple sample inventions (e.g., AI classroom assistant, sustainable energy device, medical diagnostic tool).
- Run the full graph for each scenario and save example outputs in docs/ or notebooks/.
- Adjust prompts, retrieval parameters, or graph flow based on test results to improve clarity and usefulness.

[DONE] Step 11: Document the project and alignment with MAT496 concepts
- Write an Overview section describing the Invention Assistant and its purpose.
- Explain how the project uses prompting, structured output, semantic search, RAG, tool calling, and LangGraph (state + nodes + graph).
- Add usage instructions (how to run the graph, how to add more data) to the README or report file.

[DONE] Step 12: Final cleanup and preparation for submission
- Review and refactor the code for readability and comments.
- Ensure [TODO] markers are changed to [DONE] for all completed steps before final commit.
- Check commit history shows work spread across at least two different dates.
- Verify all required files (code, plan, report, sample outputs) are pushed to the forked repository.


## Running the LangGraph in Studio

You can visualize and interact with the Invention Assistant graph in LangGraph Studio:

### Starting the Studio

1. Navigate to the studio directory:
   ```bash
   cd studio
   ```

2. Run the LangGraph development server:
   ```bash
   langgraph dev
   ```

3. Open your browser and navigate to the provided local URL (typically `http://localhost:8000`) to see the graph visualization and interact with it in the studio interface.

### Providing Input

1. In the Studio interface, you'll see an **Input** section with multiple fields.

2. **Only fill in the first field**: `{ } Invention` (marked as "Required")

3. Click on the `Invention` field and enter your invention as a JSON object:
   ```json
   {
     "title": "Your Invention Title",
     "description": "Detailed description of your invention and how it works",
     "category": "Category name (e.g., Health, Energy, Transportation)"
   }
   ```

4. **Leave all other fields empty** - they are output fields that will be automatically populated by the graph:
   - Engineer Analysis
   - Philosopher Analysis
   - Economist Analysis
   - Visionary Analysis
   - Transcript
   - Aggregated Scorecard
   - Errors
   - Feedback

### Example Inventions to Try

**Good Invention (should get "approve"):**
```json
{
  "title": "AI-Powered Smart Water Bottle",
  "description": "A water bottle with built-in sensors that track hydration levels, remind users to drink water, and sync with a mobile app to provide personalized hydration recommendations based on activity level and weather.",
  "category": "Health & Wellness"
}
```

**Problematic Invention (should trigger refinement loop):**
```json
{
  "title": "Perpetual Motion Machine",
  "description": "A device that runs forever without any energy input, using magnets arranged in a special configuration to generate unlimited free energy. This violates the laws of thermodynamics but uses a revolutionary new magnetic arrangement.",
  "category": "Energy"
}
```

### Executing the Graph

1. After entering your invention, click the **Submit** button at the bottom.

2. Watch the graph visualization at the top - you'll see nodes light up as they execute:
   - **First**: All 4 analysts (engineer, philosopher, economist, visionary) run in parallel
   - **Pause**: The graph will pause at the `aggregate` node (this is an interrupt for debugging)
   - **Continue**: Click the **Continue** button to proceed

3. The aggregate node will make a decision:
   - **approve** (score ≥ 3.5): Good invention, proceed with development
   - **revise** (score ≥ 3.0): Needs improvement, address concerns
   - **reject** (score < 3.0): Triggers the refinement loop

### Understanding the Refinement Loop

If the invention gets a **"reject"** decision:

1. The graph routes to the **refine** node
2. Feedback is generated for the analysts
3. All 4 analysts run again with the feedback
4. The graph aggregates a second time
5. The graph ends (only one refinement iteration to prevent infinite loops)

You can see this cycle in the graph visualization - the execution path will show the flow through the refine node and back to the analysts.

### Viewing Results

- **Expand nodes**: Click the `>` arrow next to any node to see its output
- **Check scores**: Look at the Aggregated Scorecard to see ratings for:
  - Technical Rigor
  - Originality
  - Feasibility
  - Impact
- **Read transcript**: See the combined analysis from all four personas
- **Review decision**: Check the overall decision and rationale


## Conclusion:

I had planned to build a robust, multi-agent evaluation system, and I believe I have achieved this conclusion satisfactorily. The system successfully integrates four distinct personas, uses RAG to ground their knowledge, and implements a sophisticated feedback loop that mimics real-world iterative review processes. The LangGraph visualization clearly shows the parallel execution and conditional routing, confirming that the architecture works as designed. The ability to handle both "good" and "bad" inventions with appropriate routing (approval vs. refinement) demonstrates the flexibility and intelligence of the agentic workflow.

----------

# Added instructions:

- This is a `solo assignment`. Each of you will work alone. You are free to talk, discuss with chatgpt, but you are responsible for what you submit. Some students may be called for viva. You should be able to each and every line of work submitted by you.

- `commit` History maintenance.
  - Fork this respository and build on top of that.
  - For every step in your plan, there has to be a commit.
  - Change [TODO] to [DONE] in the plan, before you commit after that step. 
  - The commit history should show decent amount of work spread into minimum two dates. 
  - **All the commits done in one day will be rejected**. Even if you are capable of doing the whole thing in one day, refine it in two days.  
 
 - Deadline: Nov 30, Sunday 11:59 pm


# Grading: total 25 marks

- Coverage of most of topics in this class: 20
- Creativity: 5