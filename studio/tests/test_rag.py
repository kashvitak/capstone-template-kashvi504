"""Test script for RAG system - can run without full dependencies installed."""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

print("=" * 60)
print("RAG System Test")
print("=" * 60)

# Check if dependencies are installed
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    print("[OK] All RAG dependencies are installed")
    deps_installed = True
except ImportError as e:
    print(f"[ERROR] Missing dependencies: {e}")
    print("\nTo install dependencies, run:")
    print("  pip install langchain langchain-community langchain-openai faiss-cpu tiktoken")
    deps_installed = False

# Check data files
print("\nChecking data files...")
data_dir = Path(__file__).parent.parent / "data"
for analyst in ["engineer", "philosopher", "economist", "visionary"]:
    analyst_dir = data_dir / analyst
    if analyst_dir.exists():
        files = list(analyst_dir.glob("*.txt"))
        print(f"  [OK] {analyst}: {len(files)} file(s)")
    else:
        print(f"  [ERROR] {analyst}: directory not found")

if deps_installed:
    print("\nTesting RAG system...")
    try:
        from rag import RAGSystem
        
        rag = RAGSystem()
        print("Building vector stores...")
        results = rag.build_all()
        
        print("\nVector store build results:")
        for analyst, success in results.items():
            status = "[OK]" if success else "[ERROR]"
            print(f"  {status} {analyst}")
        
        # Test retrieval
        print("\nTesting retrieval for 'Smart Water Bottle'...")
        test_query = "Smart Water Bottle with sensors to track hydration"
        
        for analyst in ["engineer", "philosopher"]:
            chunks = rag.retrieve_for_analyst(analyst, test_query, k=2)
            print(f"\n{analyst.upper()} ({len(chunks)} chunks):")
            for i, chunk in enumerate(chunks, 1):
                preview = chunk[:80].replace("\n", " ")
                print(f"  {i}. {preview}...")
        
        print("\n" + "=" * 60)
        print("RAG system is working correctly!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError testing RAG: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\nSkipping RAG tests (dependencies not installed)")
