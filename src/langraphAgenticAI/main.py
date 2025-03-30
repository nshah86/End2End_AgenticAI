import os
import sys
import streamlit as st

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.langraphAgenticAI.ui.streamlitui.loadui import LoadStreamUI
from src.langraphAgenticAI.graph.graph_builder import GraphBuilder
from src.langraphAgenticAI.LLMS.groqllm import GroqLLM

def initialize_graph(user_controls):
    """
    Initialize a LangGraph with the appropriate LLM.
    
    Args:
        user_controls (dict): User configuration options.
        
    Returns:
        object: A compiled LangGraph.
    """
    # Get LLM based on user selection
    llm_provider = user_controls.get("llm_provider", "Groq")
    
    if llm_provider == "Groq":
        # Initialize Groq LLM
        llm_handler = GroqLLM(user_controls)
        llm = llm_handler.get_llm_model()
        
        if not llm:
            st.error("Failed to initialize the LLM. Please check your API key and configuration.")
            return None
        
        # Create graph builder with the LLM
        graph_builder = GraphBuilder(llm)
        
        # Build a basic chatbot graph
        graph = graph_builder.basic_chatbot_build_graph()
        
        return graph
    
    else:
        st.error(f"LLM provider {llm_provider} not implemented yet.")
        return None

def main():
    """Main entry point for the application."""
    ui = LoadStreamUI()
    
    # Set up the callback to create and run the graph
    def process_message(message):
        """
        Process a message using the LangGraph.
        
        Args:
            message (str): User message to process.
            
        Returns:
            str: Generated response.
        """
        # Initialize the graph with current user controls
        graph = initialize_graph(ui.user_controls)
        
        if not graph:
            return "Error: Failed to initialize the graph. Please check your configuration."
        
        # Run the graph with the input message
        result = graph.invoke({
            "messages": [{"role": "user", "content": message}]
        })
        
        # Extract the AI response from the result
        if result and result.get("messages"):
            ai_messages = [msg for msg in result["messages"] if msg["role"] == "assistant"]
            if ai_messages:
                return ai_messages[-1]["content"]
        
        return "Error: Failed to generate a response."
    
    # Set the message processor in the UI
    ui.message_processor = process_message
    
    # Run the UI
    ui.run()

if __name__ == "__main__":
    main()


#