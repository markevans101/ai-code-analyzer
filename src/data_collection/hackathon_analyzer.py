import requests
from urllib.parse import urlparse
import re
import time

class HackathonProjectAnalyzer:
    def __init__(self, github_url):
        self.github_url = github_url
        self.github_token = "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"
        self.owner = None
        self.repo = None
        self.basic_info = None
        self.rag_analysis = None
        self.headers = {'Authorization': f'token {self.github_token}'}

    def validate_github_url(self):
        try:
            parsed = urlparse(self.github_url)
            if 'github.com' not in parsed.netloc:
                return False, "Not a GitHub URL"
            
            parts = parsed.path.strip('/').split('/')
            if len(parts) < 2:
                return False, "Invalid repository path"
            
            self.owner = parts[0]
            self.repo = parts[1]
            return True, None
            
        except Exception as e:
            return False, f"Error parsing URL: {str(e)}"

    def get_basic_info(self):
        api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}"
        
        try:
            print("  Fetching repository metadata...")
            response = requests.get(api_url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                self.basic_info = {
                    'name': data['name'],
                    'description': data['description'],
                    'stars': data['stargazers_count'],
                    'language': data['language'],
                    'created_at': data['created_at'],
                    'last_updated': data['updated_at'],
                    'topics': data.get('topics', []),
                    'url': data['html_url']
                }
                print("  ✓ Basic info retrieved successfully")
                return True
            print(f"  ✗ Error: API returned status code {response.status_code}")
            return False
        except Exception as e:
            print(f"  ✗ Error getting basic info: {str(e)}")
            return False

    def get_python_files(self, path=''):
        files = []
        api_url = f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/{path}"
        
        try:
            print(f"  Scanning directory: {path or 'root'}")
            response = requests.get(api_url, headers=self.headers)
            if response.status_code == 200:
                contents = response.json()
                
                if not isinstance(contents, list):
                    contents = [contents]
                    
                for item in contents:
                    if item['type'] == 'file' and item['name'].endswith('.py'):
                        files.append(item['download_url'])
                        print(f"    Found Python file: {item['name']}")
                    elif item['type'] == 'dir':
                        files.extend(self.get_python_files(item['path']))
            return files
        except Exception as e:
            print(f"  ✗ Error getting files: {str(e)}")
            return files

    def analyze_rag_components(self):
        rag_patterns = {
            'embeddings': r'embedding|sentence-transformers|text2vec',
            'vector_stores': r'chroma|pinecone|weaviate|faiss|qdrant',
            'retrievers': r'retriever|BM25|semantic_search',
            'llm_usage': r'openai|gpt-|llama|anthropic|claude',
            'frameworks': r'langchain|llamaindex|haystack',
            'prompt_templates': r'prompt_template|system_message',
            'memory_components': r'memory|conversation_buffer',
            'document_loaders': r'document_loader|text_splitter'
        }
        
        self.rag_analysis = {
            'rag_components_found': [],
            'frameworks_detected': [],
            'python_files_analyzed': 0,
            'rag_related_files': 0
        }
        
        try:
            print("\nScanning repository structure...")
            python_files = self.get_python_files()
            print(f"\nFound {len(python_files)} Python files to analyze")
            
            for i, file_url in enumerate(python_files, 1):
                print(f"\nAnalyzing file {i}/{len(python_files)}: {file_url.split('/')[-1]}")
                self.rag_analysis['python_files_analyzed'] += 1
                
                file_response = requests.get(file_url, headers=self.headers)
                if file_response.status_code == 200:
                    content = file_response.text
                    
                    for component, pattern in rag_patterns.items():
                        if re.search(pattern, content, re.IGNORECASE):
                            if component == 'frameworks':
                                matches = re.findall(pattern, content, re.IGNORECASE)
                                self.rag_analysis['frameworks_detected'].extend(matches)
                                print(f"  ✓ Found framework: {matches}")
                            else:
                                self.rag_analysis['rag_components_found'].append(component)
                                print(f"  ✓ Found component: {component}")
                            self.rag_analysis['rag_related_files'] += 1
                            break
                time.sleep(0.1)  # Small delay to avoid rate limiting
            
            self.rag_analysis['rag_components_found'] = list(set(self.rag_analysis['rag_components_found']))
            self.rag_analysis['frameworks_detected'] = list(set(self.rag_analysis['frameworks_detected']))
            return True
            
        except Exception as e:
            print(f"  ✗ Error analyzing RAG components: {str(e)}")
            return False

    def analyze(self):
        print(f"\nAnalyzing repository: {self.github_url}")
        
        is_valid, error = self.validate_github_url()
        if not is_valid:
            print(f"Error: {error}")
            return False
            
        print("\nGetting basic repository information...")
        if not self.get_basic_info():
            print("Error getting basic repository information")
            return False
            
        print("\nAnalyzing RAG components...")
        if not self.analyze_rag_components():
            print("Error analyzing RAG components")
            return False
            
        return True

    def print_results(self):
        if not (self.basic_info and self.rag_analysis):
            print("No analysis results available")
            return
            
        print("\n=== Repository Information ===")
        for key, value in self.basic_info.items():
            print(f"{key}: {value}")
            
        print("\n=== RAG Analysis ===")
        for key, value in self.rag_analysis.items():
            print(f"{key}: {value}")

# Test the analyzer
if __name__ == "__main__":
    test_url = "https://github.com/hwchase17/chat-langchain"  # Smaller test repository
    analyzer = HackathonProjectAnalyzer(test_url)
    
    if analyzer.analyze():
        analyzer.print_results()

    def analyze_with_agent(self, code):
        """Use the CodeAnalyzerAgent to analyze code."""
        try:
            from src.agents.code_analyzer_agent import CodeAnalyzerAgent
            
            # You'll need to set your OpenAI API key
            agent = CodeAnalyzerAgent(openai_api_key="your-key-here")
            
            results = agent.analyze(
                code=code,
                objective="Analyze this code for RAG implementation patterns and quality"
            )
            
            return results
        except Exception as e:
            print(f"Error using agent: {str(e)}")
            return None
