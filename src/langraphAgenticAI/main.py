import os
import sys
import streamlit as st

# Add debugging to see environment variables
print("Current working directory:", os.getcwd())
print("Checking if .env file exists:", os.path.exists(".env"))

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.langraphAgenticAI.ui.streamlitui.loadui import LoadStreamUI
from src.langraphAgenticAI.graph.graph_builder import GraphBuilder
from src.langraphAgenticAI.LLMS.groqllm import GroqLLM
from src.langraphAgenticAI.utils.env_loader import load_env_variables, get_env_var
from src.langraphAgenticAI.loadui import load_ui

# Load environment variables from .env file
load_env_variables()

# Debug: Print all environment variables to check if loading worked
print("After loading .env, GROQ_API_KEY exists:", "GROQ_API_KEY" in os.environ)
if "GROQ_API_KEY" in os.environ:
    print("GROQ_API_KEY value length:", len(os.environ["GROQ_API_KEY"]))
else:
    print("GROQ_API_KEY not found in environment variables")

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
    # Load UI and get user inputs
    ui_data = load_ui()
    
    # Initialize GroqLLM with user controls
    groq_llm = GroqLLM(ui_data["user_controls"])
    
    # Handle chat input
    if ui_data["user_input"]:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": ui_data["user_input"]})
        
        # Display the user message
        with st.chat_message("user"):
            st.markdown(ui_data["user_input"])
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            try:
                # Get response from GroqLLM
                response = groq_llm.generate_response(ui_data["user_input"])
                
                # Update placeholder with response
                message_placeholder.markdown(response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                message_placeholder.markdown(f"Error: {str(e)}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})

if __name__ == "__main__":
    main()


#