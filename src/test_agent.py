from agents.code_analyzer_agent import CodeAnalyzerAgent
from config import TOGETHER_API_KEY

# Test code
test_code = """
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def setup_rag():
    with open('data.txt', 'r') as f:
        raw_text = f.read()
    
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_text(raw_text)
    
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_texts(texts, embeddings)
    
    retriever = db.as_retriever()
    
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=retriever
    )
    
    return qa
"""
def main():
    print("Initializing agent...")
    agent = CodeAnalyzerAgent(TOGETHER_API_KEY)
    
    print("\nAnalyzing code...")
    objective = "Analyze this code for RAG patterns and code quality"
    results = agent.analyze(test_code, objective)
    
    print("\nResults:")
    print(results)

if __name__ == "__main__":
    main()
