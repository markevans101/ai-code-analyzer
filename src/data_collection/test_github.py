from src.data_collection.github_analyzer import GitHubAnalyzer

def main():
    analyzer = GitHubAnalyzer()
    df = analyzer.search_hackathon_repos(limit=10)
    
    if df is not None:
        print(f"Found {len(df)} repositories")
        print("
Sample data:")
        print(df[["name", "description", "stars"]].head())

if __name__ == "__main__":
    main()
