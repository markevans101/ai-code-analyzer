from rag_system import RAGSystem
import unittest

def test_rag():
    try:
        rag = RAGSystem()
        result = rag.ask("What is the capital of France?")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_rag()
