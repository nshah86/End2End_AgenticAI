import os
import sys
import streamlit as st

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.langraphAgenticAI.ui.streamlitui.loadui import LoadStreamUI

def main():
    """Main entry point for the application."""
    ui = LoadStreamUI()
    ui.run()

if __name__ == "__main__":
    main()
