import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.langraphAgenticAI.app import main

if __name__ == "__main__":
    main() 