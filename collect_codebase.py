import os
from pathlib import Path

def collect_codebase(output_file='project_codebase.txt'):
    """Collect all project files into a single text file."""
    
    # File extensions to include
    EXTENSIONS = {'.py', '.md', '.txt', '.json'}
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    with open(output_file, 'w') as out:
        # Walk through all directories
        for root, dirs, files in os.walk(project_root):
            # Skip __pycache__ and .git directories
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'env', 'venv']]
            
            for file in files:
                file_path = Path(root) / file
                
                # Check if file extension should be included
                if file_path.suffix in EXTENSIONS:
                    # Write file path as header
                    relative_path = file_path.relative_to(project_root)
                    out.write(f"\n{'='*80}\n")
                    out.write(f"File: {relative_path}\n")
                    out.write(f"{'='*80}\n\n")
                    
                    # Write file contents
                    try:
                        with open(file_path, 'r') as f:
                            out.write(f.read())
                        out.write('\n\n')
                    except Exception as e:
                        out.write(f'Error reading file: {e}\n\n')

if __name__ == "__main__":
    collect_codebase()
    print("Codebase collected in project_codebase.txt")