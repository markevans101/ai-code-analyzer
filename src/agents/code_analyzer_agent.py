from langchain_community.llms import Together
import time

class CodeAnalyzerAgent:
    def __init__(self, together_api_key):
        self.llm = Together(
            model='mistralai/Mixtral-8x7B-Instruct-v0.1',
            together_api_key=together_api_key,
            temperature=0.1,
            max_tokens=2048
        )
        
    def analyze(self, code, objective):
        try:
            prompt = 'Show code examples for improving this RAG implementation. Include error handling and tests. Code to analyze: ' + str(code)
            return self.llm.invoke(prompt)
        except Exception as e:
            return 'Error: ' + str(e)
