import streamlit as st
from code_analyzer import CodeAnalyzer
import os

def main():
    st.title("AI Code Analyzer")
    st.write("Analyze your Python code and get improvement suggestions!")
    
    code = st.text_area("Enter your Python code:", height=200)
    
    st.write("Select focus areas:")
    focus_areas = []
    cols = st.columns(3)
    for i, area in enumerate(CodeAnalyzer.FOCUS_AREAS.keys()):
        if cols[i % 3].checkbox(area):
            focus_areas.append(area)
    
    if st.button("Analyze Code"):
        if not code:
            st.error("Please enter some code to analyze")
            return
        
        try:
            with st.spinner("Analyzing code..."):
                analyzer = CodeAnalyzer()
                result = analyzer.analyze(code, focus_areas if focus_areas else None)
                
                st.write("### Analysis Results")
                st.write(f"**Overview:** {result['description']}")
                
                if result['suggestions']:
                    for suggestion in result['suggestions']:
                        with st.expander(f"[{suggestion['severity']}] {suggestion['issue']}"):
                            st.write(f"**Solution:** {suggestion['solution']}")
                            if suggestion['code'] and suggestion['code'] != 'N/A':
                                code = suggestion['code']
                                code = code.replace('```python', '').replace('```', '').strip()
                                st.code(code, language="python")
                else:
                    st.info("No suggestions found.")
                    
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
    
    st.markdown("---")
    st.markdown("Made with ❤️ using AI")

if __name__ == "__main__":
    main()
