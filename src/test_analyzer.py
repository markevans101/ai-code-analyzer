from code_analyzer import CodeAnalyzer

def test_basic_analysis():
    # Sample code to analyze
    sample_code = """
def divide(a, b):
    return a / b

def main():
    x = 10
    y = 0
    result = divide(x, y)
    print(result)
"""

    try:
        # Create analyzer and run analysis
        analyzer = CodeAnalyzer()
        
        # Analyze with multiple focus areas
        result = analyzer.analyze(
            code=sample_code,
            focus_areas=['error_handling', 'testing']
        )
        
        # Print formatted results
        formatted = analyzer.format_report(result)
        print("\nAnalysis Results:")
        print(formatted)
        
        # Save to file
        report_file = analyzer.save_report(result, "analysis_report.txt")
        print(f"\nReport saved to: {report_file}")
        
        # Print available focus areas
        print("\nAvailable focus areas:")
        for area in CodeAnalyzer.FOCUS_AREAS:
            print(f"- {area}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_basic_analysis()
