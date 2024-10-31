import argparse
from code_analyzer import CodeAnalyzer
import os
import json

def print_summary(result):
    """Print a concise summary of the analysis"""
    try:
        data = json.loads(result)
        print("\nSummary of Analysis:")
        print("-------------------")
        print(f"Overview: {data['description']}")
        print("\nKey Suggestions:")
        for i, suggestion in enumerate(data['suggestions'], 1):
            severity = suggestion.get('severity', 'MEDIUM')
            print(f"{i}. [{severity}] {suggestion['message']}")
    except:
        print("\nRaw Analysis:")
        print(result)

def main():
    parser = argparse.ArgumentParser(description='Analyze Python code for improvements')
    parser.add_argument('path', help='File or directory to analyze')
    parser.add_argument('--focus', choices=['error_handling', 'testing', 'structure'], 
                      help='Focus area for analysis')
    parser.add_argument('--output', help='Output file for the report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    args = parser.parse_args()

    try:
        analyzer = CodeAnalyzer()
        
        # Determine if path is file or directory
        if os.path.isfile(args.path):
            print(f"\nAnalyzing file: {args.path}")
            result = analyzer.analyze_file(args.path, args.focus)
        elif os.path.isdir(args.path):
            print(f"\nAnalyzing directory: {args.path}")
            result = analyzer.analyze_directory(args.path, args.focus)
        else:
            raise ValueError(f"Path not found: {args.path}")

        # Print summary to console
        if isinstance(result, dict):
            for file_path, analysis in result.items():
                print(f"\nResults for {file_path}:")
                print_summary(analysis)
        else:
            print_summary(result)

        # Save report
        output_file = args.output or f"analysis_report_{os.path.basename(args.path)}.txt"
        report_path = analyzer.save_report(result, output_file)
        print(f"\nFull analysis saved to: {report_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
