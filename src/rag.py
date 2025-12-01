"""RAG (Retrieval Augmented Generation) module for Invention Assistant.

This module handles:
1. Loading and chunking reference documents
2. Creating embeddings and vector store
3. Retrieving relevant context for analyst queries
"""
import os
from pathlib import Path
from typing import List, Dict, Any
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Type hints that depend on langchain
Document = None
RAG_AVAILABLE = False

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    from langchain_core.documents import Document
    RAG_AVAILABLE = True
except ImportError as e:
    logging.warning(f"RAG dependencies not installed: {e}")
    logging.warning("Install with: pip install langchain langchain-community langchain-openai faiss-cpu")


class AnalystRAG:
    """RAG system for a single analyst persona."""
    
    def __init__(self, analyst_name: str, data_dir: Path):
        """Initialize RAG for a specific analyst.
        
        Args:
            analyst_name: Name of the analyst (engineer, philosopher, economist, visionary)
            data_dir: Path to the data directory for this analyst
        """
        self.analyst_name = analyst_name
        self.data_dir = data_dir
        self.vector_store = None
        self.embeddings = None
        
    def load_documents(self) -> List[Document]:
        """Load all text files from the analyst's data directory."""
        documents = []
        
        if not RAG_AVAILABLE:
            logging.warning(f"RAG dependencies not available, cannot load documents for {self.analyst_name}")
            return documents
        
        if not self.data_dir.exists():
            logging.warning(f"Data directory does not exist: {self.data_dir}")
            return documents
            
        for file_path in self.data_dir.glob("*.txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    doc = Document(
                        page_content=content,
                        metadata={"source": file_path.name, "analyst": self.analyst_name}
                    )
                    documents.append(doc)
                    logging.info(f"Loaded {file_path.name} for {self.analyst_name}")
            except Exception as e:
                logging.error(f"Error loading {file_path}: {e}")
                
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks for better retrieval."""
        if not RAG_AVAILABLE:
            logging.warning(f"RAG dependencies not available, cannot chunk documents for {self.analyst_name}")
            return []
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        logging.info(f"Created {len(chunks)} chunks for {self.analyst_name}")
        return chunks
    
    def build_vector_store(self):
        """Build FAISS vector store from documents."""
        if not RAG_AVAILABLE:
            logging.warning(f"RAG dependencies not available, cannot build vector store for {self.analyst_name}")
            return False
        
        try:
            # Load and chunk documents
            documents = self.load_documents()
            if not documents:
                logging.warning(f"No documents found for {self.analyst_name}")
                return False
                
            chunks = self.chunk_documents(documents)
            
            # Create embeddings and vector store
            # Create embeddings (using text-embedding-3-small for cost/performance balance)
            self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
            
            logging.info(f"Built vector store for {self.analyst_name} with {len(chunks)} chunks")
            return True
            
        except Exception as e:
            logging.error(f"Error building vector store for {self.analyst_name}: {e}")
            return False
    
    def retrieve(self, query: str, k: int = 3) -> List[str]:
        """Retrieve top-k relevant chunks for a query.
        
        Args:
            query: The search query
            k: Number of chunks to retrieve
            
        Returns:
            List of relevant text chunks
        """
        if self.vector_store is None:
            logging.info(f"Vector store not initialized for {self.analyst_name}, attempting to build...")
            success = self.build_vector_store()
            if not success:
                logging.warning(f"Failed to build vector store for {self.analyst_name}")
                return []
            
        try:
            docs = self.vector_store.similarity_search(query, k=k)
            chunks = [doc.page_content for doc in docs]
            logging.info(f"Retrieved {len(chunks)} chunks for query: {query[:50]}...")
            return chunks
        except Exception as e:
            logging.error(f"Error retrieving chunks: {e}")
            return []


class RAGSystem:
    """Manages RAG for all analyst personas."""
    
    def __init__(self, data_root: Path = None):
        """Initialize RAG system for all analysts.
        
        Args:
            data_root: Root directory containing analyst subdirectories
        """
        if data_root is None:
            data_root = Path(__file__).parent.parent / "data"
        
        self.data_root = Path(data_root)
        self.analysts = {}
        
        # Initialize RAG for each analyst
        for analyst_name in ["engineer", "philosopher", "economist", "visionary"]:
            analyst_dir = self.data_root / analyst_name
            self.analysts[analyst_name] = AnalystRAG(analyst_name, analyst_dir)
    
    def build_all(self):
        """Build vector stores for all analysts."""
        logging.info("Building vector stores for all analysts...")
        results = {}
        for name, rag in self.analysts.items():
            results[name] = rag.build_vector_store()
        return results
    
    def retrieve_for_analyst(self, analyst_name: str, query: str, k: int = 3) -> List[str]:
        """Retrieve relevant context for a specific analyst.
        
        Args:
            analyst_name: Name of the analyst
            query: The invention description or query
            k: Number of chunks to retrieve
            
        Returns:
            List of relevant text chunks
        """
        if analyst_name not in self.analysts:
            logging.warning(f"Unknown analyst: {analyst_name}")
            return []
        
        return self.analysts[analyst_name].retrieve(query, k=k)


# Singleton instance
_rag_system = None

def get_rag_system() -> RAGSystem:
    """Get or create the global RAG system instance."""
    global _rag_system
    if _rag_system is None:
        _rag_system = RAGSystem()
        _rag_system.build_all()
    return _rag_system


if __name__ == "__main__":
    # Test the RAG system
    logging.basicConfig(level=logging.INFO)
    
    rag = RAGSystem()
    results = rag.build_all()
    
    print("\nVector store build results:")
    for analyst, success in results.items():
        status = "✓" if success else "✗"
        print(f"  {status} {analyst}")
    
    # Test retrieval
    print("\nTest retrieval for 'Smart Water Bottle':")
    for analyst in ["engineer", "philosopher", "economist", "visionary"]:
        chunks = rag.retrieve_for_analyst(analyst, "Smart Water Bottle with sensors", k=2)
        print(f"\n{analyst.upper()}:")
        for i, chunk in enumerate(chunks, 1):
            print(f"  Chunk {i}: {chunk[:100]}...")
