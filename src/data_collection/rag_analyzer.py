import requests
import base64
import re

def get_python_files(owner, repo, path=''):
    """Recursively get all Python files from a repository."""
    files = []
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            contents = response.json()
            
            # Handle if response is a list (directory) or dict (file)
            if not isinstance(contents, list):
                contents = [contents]
                
            for item in contents:
                if item['type'] == 'file' and item['name'].endswith('.py'):
                    files.append(item['download_url'])
                elif item['type'] == 'dir':
                    # Recursively get files from subdirectories
                    files.extend(get_python_files(owner, repo, item['path']))
        return files
    except Exception as e:
        print(f"Error getting files: {str(e)}")
        return files

def analyze_rag_components(owner, repo):
    """Analyze a repository for RAG-related components."""
    
    # Common RAG-related patterns to look for
    rag_patterns = {
        'embeddings': r'embedding|sentence-transformers|text2vec',
        'vector_stores': r'chroma|pinecone|weaviate|faiss|qdrant',
        'retrievers': r'retriever|BM25|semantic_search',
        'llm_usage': r'openai|gpt-|llama|anthropic|claude',
        'frameworks': r'langchain|llamaindex|haystack'
    }
    
    # Initialize results
    rag_analysis = {
        'rag_components_found': [],
        'frameworks_detected': [],
        'python_files_analyzed': 0,
        'rag_related_files': 0
    }
    
    try:
        # Get all Python files
        python_files = get_python_files(owner, repo)
        
        # Analyze each file
        for file_url in python_files:
            rag_analysis['python_files_analyzed'] += 1
            
            # Get file content
            file_response = requests.get(file_url)
            if file_response.status_code == 200:
                content = file_response.text
                
                # Check for RAG patterns
                for component, pattern in rag_patterns.items():
                    if re.search(pattern, content, re.IGNORECASE):
                        if component == 'frameworks':
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            rag_analysis['frameworks_detected'].extend(matches)
                        else:
                            rag_analysis['rag_components_found'].append(component)
                        rag_analysis['rag_related_files'] += 1
                        break
        
        # Remove duplicates
        rag_analysis['rag_components_found'] = list(set(rag_analysis['rag_components_found']))
        rag_analysis['frameworks_detected'] = list(set(rag_analysis['frameworks_detected']))
        
        return rag_analysis
        
    except Exception as e:
        print(f"Error analyzing RAG components: {str(e)}")
        return None

# Test the function
if __name__ == "__main__":
    test_owner = "langchain-ai"
    test_repo = "langchain"
    
    print("\nAnalyzing RAG components...")
    print("This may take a few minutes for large repositories...")
    results = analyze_rag_components(test_owner, test_repo)
    
    if results:
        print("\nAnalysis Results:")
        for key, value in results.items():
            print(f"{key}: {value}")
