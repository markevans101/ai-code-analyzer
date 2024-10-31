content = '''from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import os

class RAGSystem:
    def __init__(self, file_path=data.txt):
        if not os.path.exists(file_path):
            raise FileNotFoundError(fData file not found: {file_path})
            
        try:
            with open(file_path, r) as f:
                raw_text = f.read()
                
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            texts = text_splitter.split_text(raw_text)
            
            embeddings = OpenAIEmbeddings()
            self.db = Chroma.from_texts(texts, embeddings)
            self.qa = self._setup_qa()
            
        except Exception as e:
            raise Exception(fFailed to initialize RAG system: {e})
            
    def _setup_qa(self):
        try:
            retriever = self.db.as_retriever()
            return RetrievalQA.from_chain_type(
                llm=OpenAI(),
                chain_type=stuff,
                retriever=retriever
            )
        except Exception as e:
            raise Exception(fFailed to setup QA system: {e})
            
    def ask(self, question):
        try:
            response = self.qa({question: question})
            return response[result]
        except Exception as e:
            return fError processing question: {e}
'''

with open(src/rag_system.py, w) as f:
    f.write(content)
