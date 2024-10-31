import streamlit as st
from code_analyzer import CodeAnalyzer
import os

def main():
    st.title("AI Code Analyzer")
    st.write("Analyze your Python code and get 
improvement suggestions!")

    # Code input
    code = st.text_area("Enter your Python code:", 
height=200)

    # Focus areas selection
    st.write("Select focus areas:")
    focus_areas = []
    cols = st.columns(3)
    for i, area in 
enumerate(CodeAnalyzer.FOCUS_AREAS.keys()):
        if cols[i % 3].checkbox(area):
            focus_areas.append(area)

    # Analyze button
    if st.button("Analyze Code"):
        if not code:
            st.error("Please enter some code to 
analyze")
            return

        try:
            with st.spinner("Analyzing code..."):
                analyzer = CodeAnalyzer()  # Will use 
environment variable from Streamlit
                result = analyzer.analyze(code, 
focus_areas if focus_areas else None)
                
                # Display results
                st.write("### Analysis Results")
                st.write(f"**Overview:** 
{result['description']}")
                
                # Display suggestions by category
                if result['suggestions']:
                    for suggestion in 
result['suggestions']:
                        with 
st.expander(f"[{suggestion['severity']}] 
{suggestion['issue']}"):
                            st.write(f"**Solution:** 
{suggestion['solution']}")
                            st.code(suggestion['code'], 
language="python")
                else:
                    st.info("No suggestions found.")

        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

    # Add footer
    st.markdown("---")
    st.markdown("Made with ❤️ using AI")

if __name__ == "__main__":
    main()
