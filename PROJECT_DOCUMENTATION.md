# Invention Assistant - Multi-Persona AI Evaluation System

## Project Overview

The **Invention Assistant** is an intelligent system that evaluates invention ideas through the perspectives of four distinct analyst personas: Engineer, Philosopher, Economist, and Visionary. Built using LangGraph and powered by Retrieval Augmented Generation (RAG), the system provides comprehensive, multi-dimensional analysis of invention proposals.

### Key Features:
- **Multi-Persona Analysis**: Four specialized AI analysts evaluate inventions from different angles:
  - **Engineer**: Technical feasibility, implementation challenges, and safety considerations
  - **Philosopher**: Ethical implications, societal impact, and moral frameworks
  - **Economist**: Market viability, cost-benefit analysis, and economic sustainability
  - **Visionary**: Future potential, transformative impact, and long-term scenarios

- **RAG-Enhanced Insights**: Each analyst is equipped with domain-specific knowledge retrieved from curated reference documents using semantic search (FAISS vector store + OpenAI embeddings)

- **Structured Evaluation**: Generates detailed scorecards across four dimensions:
  - Technical Rigor
  - Originality
  - Feasibility
  - Impact

- **Professional Reports**: Outputs comprehensive Markdown reports with evidence-based recommendations and final decisions (Approve/Revise/Reject)

## Alignment with MAT496 Course Content

This project demonstrates mastery of all major topics covered in MAT496:

### 1. **Prompting**
- Designed specialized system prompts for each analyst persona
- Crafted prompts that elicit structured, JSON-formatted responses
- Integrated RAG context into prompts for domain-grounded analysis
- See: `src/prompts.py` for all persona prompts

### 2. **Structured Output**
- Enforced consistent JSON schema for all analyst responses
- Implemented transcript format with role, message, and citations
- Created standardized scorecard structure with scores and evidence
- See: `src/invention_assistant_graph.py` - `InventionState` TypedDict

### 3. **Semantic Search**
- Built FAISS vector stores for each analyst's knowledge domain
- Used OpenAI embeddings to convert text into semantic vectors
- Implemented similarity search to retrieve relevant context chunks
- See: `src/rag.py` - `AnalystRAG.retrieve()` method

### 4. **Retrieval Augmented Generation (RAG)**
- Collected domain-specific reference documents for each analyst (`data/` directory)
- Preprocessed and chunked documents using `RecursiveCharacterTextSplitter`
- Integrated retrieval into the analysis pipeline to ground responses in factual knowledge
- See: `src/rag.py` - Complete RAG implementation

### 5. **LangGraph: State, Nodes, Graph**
- **State**: Defined `InventionState` TypedDict with proper field annotations and reducers
- **Nodes**: Created individual node functions for each analyst persona + aggregation node
- **Graph**: Built a StateGraph with parallel execution (all analysts run simultaneously)
- Implemented proper edge definitions (START → analysts → aggregate → END)
- See: `src/invention_assistant_graph.py` - `create_invention_graph()` function

### 6. **Tool Calling & MCP** (Bonus)
- While not explicitly using MCP servers, the system demonstrates modular tool design
- Each analyst can be viewed as a "tool" that processes invention descriptions
- The RAG system acts as a retrieval tool integrated into the workflow

## How to Use

### Prerequisites
```bash
pip install -r requirements.txt
```

Set up your OpenAI API key in a `.env` file:
```
OPENAI_API_KEY=your_key_here
```

### Running the System

#### Option 1: Using the Demo Notebook
```bash
jupyter notebook notebooks/invention_assistant_demo.ipynb
```

#### Option 2: Using LangGraph Studio
```bash
cd studio
langgraph dev
```

#### Option 3: Programmatically
```python
from src.invention_assistant_graph import run_all_analysts_parallel

invention = {
    "title": "Smart Water Bottle",
    "description": "A water bottle with sensors that track hydration levels..."
}

result = run_all_analysts_parallel(invention)
print(result["scorecard"])
```

### Project Structure
```
capstone-template-kashvi504/
├── src/
│   ├── invention_assistant_graph.py  # Main LangGraph implementation
│   ├── rag.py                        # RAG system with FAISS
│   ├── prompts.py                    # Analyst persona prompts
│   ├── report_generator.py          # Markdown report formatter
│   └── utils.py                      # LLM call utilities
├── data/
│   ├── engineer/                     # Engineering reference docs
│   ├── philosopher/                  # Ethics reference docs
│   ├── economist/                    # Market analysis docs
│   └── visionary/                    # Futures scenarios docs
├── notebooks/
│   ├── invention_assistant_demo.ipynb
│   └── outputs/                      # Sample evaluation reports
├── studio/                           # LangGraph Studio configuration
└── README.md
```

## Sample Outputs

See `notebooks/outputs/` for 90+ sample evaluation reports covering inventions like:
- Smart Water Bottle
- Biodegradable Phone Case
- AI Classroom Assistant
- Solar Powered Backpack
- Smart Composting Bin
- Voice Activated Study Lamp

Each output includes:
- JSON file with full analysis data
- Markdown report with formatted scorecard and recommendations

## Why This Project is Creative

This project applies LLM capabilities to a real-world problem: **evaluating innovation**. It automates what would typically require assembling a diverse panel of experts, making invention assessment more accessible and comprehensive. The multi-persona approach ensures balanced evaluation across technical, ethical, economic, and visionary dimensions—something that's difficult to achieve with a single LLM prompt.

## Conclusion

I successfully implemented a complete Invention Assistant system that demonstrates all major MAT496 concepts. The system:
- ✅ Uses sophisticated prompting techniques for each analyst persona
- ✅ Enforces structured JSON output with proper schemas
- ✅ Implements semantic search using FAISS and OpenAI embeddings
- ✅ Integrates RAG to ground analyses in domain knowledge
- ✅ Leverages LangGraph for parallel multi-agent orchestration
- ✅ Generates professional, evidence-based evaluation reports

The project showcases both technical mastery and creativity by solving a practical problem in innovation assessment. All code is well-documented, tested with multiple sample inventions, and ready for deployment.
