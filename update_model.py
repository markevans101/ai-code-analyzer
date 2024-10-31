import fileinput
import sys

def update_model():
    file_path = 'src/agents/code_analyzer_agent.py'
    old_model = 'model="togethercomputer/llama-2-70b-chat"'
    new_model = 'model="meta-llama/Llama-2-7b-chat-hf"'
    
    with fileinput.FileInput(file_path, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(old_model, new_model), end='')
    
    print(f"Updated model in {file_path}")

if __name__ == "__main__":
    update_model()
