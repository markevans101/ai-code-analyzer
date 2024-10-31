from langchain_community.llms import Together
import os
import json
import re
from typing import List, Dict, Optional

class CodeAnalyzer:
    FOCUS_AREAS = {
        'error_handling': 'Error handling, exception handling, input validation',
        'testing': 'Unit tests, test coverage, test cases',
        'structure': 'Code organization, readability, modularity',
        'performance': 'Code efficiency, optimization, speed',
        'security': 'Security vulnerabilities, data protection',
    }

    def __init__(self):
        api_key = os.getenv("TOGETHER_API_KEY")
        if api_key is None:
            raise ValueError("No API key provided")
                
        self.llm = Together(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            together_api_key=api_key,
            temperature=0.1,
            max_tokens=1024
        )
        
    def extract_json(self, text: str) -> Optional[dict]:
        """Extract JSON from text that might contain other content."""
        try:
            match = re.search(r'\{[\s\S]*\}', text)
            if match:
                return json.loads(match.group(0))
            return None
        except:
            return None
        
    def analyze(self, code: str, focus_areas: Optional[List[str]] = None) -> dict:
        """Analyze code with multiple focus areas."""
        if focus_areas:
            focus_str = "\n".join(f"- {area}: {self.FOCUS_AREAS[area]}"
                                for area in focus_areas
                                if area in self.FOCUS_AREAS)
        else:
            focus_str = "All aspects of code quality"

        prompt = f"""Analyze this Python code and provide detailed suggestions for 
improvements.
Return ONLY a JSON object with no additional text.

CODE:
```python
{code}
```

FOCUS AREAS:
{focus_str}

Required JSON format:
{{
    "description": "Brief overview of issues found",
    "suggestions": [
        {{
            "severity": "HIGH/MEDIUM/LOW",
            "category": "Category of the issue (e.g., error_handling, testing)",
            "issue": "Description of the issue",
            "solution": "How to fix it",
            "code": "Example fix"
        }}
    ]
}}"""

        try:
            response = self.llm.invoke(prompt)
            result = self.extract_json(response)
            if result:
                return result
            
            return {
                "description": "Could not parse response",
                "suggestions": [{
                    "severity": "HIGH",
                    "category": "error",
                    "issue": "Invalid response format",
                    "solution": "Original response below",
                    "code": response
                }]
            }
        except Exception as e:
            return {
                "description": f"Error during analysis: {str(e)}",
                "suggestions": []
            }

    def format_report(self, analysis: dict) -> str:
        output = ["=== Code Analysis Report ===\n"]
        output.append(f"Description: {analysis['description']}\n")
        
        if analysis['suggestions']:
            # Group suggestions by category
            by_category: Dict[str, List[dict]] = {}
            for s in analysis['suggestions']:
                category = s.get('category', 'general')
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(s)

            # Output suggestions by category
            for category, suggestions in by_category.items():
                output.append(f"\n{category.upper()} Suggestions:")
                for i, s in enumerate(suggestions, 1):
                    output.append(f"\n{i}. [{s['severity']}] {s['issue']}")
                    output.append(f"   Solution: {s['solution']}")
                    output.append(f"   Example Code:")
                    output.append("   ```python")
                    output.append(f"   {s['code']}")
                    output.append("   ```")
        else:
            output.append("\nNo suggestions provided.")
            
        return "\n".join(output)

    def save_report(self, analysis: dict, filename: str = "report.txt"):
        with open(filename, "w") as f:
            f.write(self.format_report(analysis))
        return filename
