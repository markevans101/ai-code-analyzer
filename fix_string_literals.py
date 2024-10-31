
def fix_file(filepath):
    """Fix unterminated string literals in a Python file."""
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Track if we found and fixed any issues
        fixed = False
        
        # Process each line
        for i, line in enumerate(lines):
            # Look for lines with odd number of quotes
            single_quotes = line.count("'")
            double_quotes = line.count('"')
            
            if single_quotes % 2 == 1 or double_quotes % 2 == 1:
                print(f"Found potential issue on line {i+1}:")
                print(f"Original: {line.rstrip()}")
                
                # Fix the line by adding missing quote
                if single_quotes % 2 == 1:
                    lines[i] = line.rstrip() + "'\n"
                if double_quotes % 2 == 1:
                    lines[i] = line.rstrip() + '"\n'
                
                print(f"Fixed to: {lines[i].rstrip()}")
                fixed = True
        
        if fixed:
            # Write the fixed content back to file
            with open(filepath, 'w', encoding='utf-8') as file:
                file.writelines(lines)
    except Exception as e:
        print(f"An error occurred while fixing the file: {e}")

# Example usage
filepath = 'test_file.py'  # Changed from 'path/to/your/file.py'
fix_file(filepath)
