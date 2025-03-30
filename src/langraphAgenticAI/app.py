import streamlit as st
from src.langraphAgenticAI.ui.streamlitui.loadui import LoadStreamUI

def main():
    """Main entry point for the application."""
    ui = LoadStreamUI()
    ui.run()

if __name__ == "__main__":
    main() 