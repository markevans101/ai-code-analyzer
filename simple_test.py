from langchain_community.llms import Together

llm = Together(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    together_api_key="ad32fc6baa04e33f3b029234462941bac3e7be45dff20dbea64fb089eb313080",
    temperature=0.1,
    max_tokens=50
)

try:
    response = llm.invoke("Please provide only the capital of France, nothing else.")
    print("Response:", response)
except Exception as e:
    print("Error:", e)
