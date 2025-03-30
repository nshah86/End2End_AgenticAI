import streamlit as st
import os
from datetime import date
from langchain_core.messages import AIMessage, HumanMessage
from src.langraphAgenticAI.ui.uiconfigfile import Config
from src.langraphAgenticAI.LLMS.groqllm import GroqLLM

class LoadStreamUI:
    def __init__(self):
        self.config = Config()
        self.llm_options = self.config.get_llm_options()
        self.user_controls = {}
        self.message_processor = None
        
    def setup_page(self):
        """Set up the Streamlit page configuration."""
        st.set_page_config(
            page_title=self.config.get('Default', 'PAGE_TITLE', 'LangGraph AI'),
            page_icon="🤖",
            layout="wide"
        )
        
    def create_sidebar(self):
        """Create the sidebar with configuration options."""
        with st.sidebar:
            st.title("Configuration")
            
            # API Key Input (hidden)
            api_key = st.text_input("API Key", type="password", 
                                    value=os.environ.get("GROQ_API_KEY", ""))
            self.user_controls["GROQ_API_KEY"] = api_key
            
            # LLM Provider Selection
            llm_provider = st.selectbox(
                "Select LLM Provider",
                options=["Groq", "OpenAI", "Anthropic"],
                index=0 if self.llm_options['llm_option'] == 'Groq' else 
                      1 if self.llm_options['llm_option'] == 'OpenAI' else 2
            )
            self.user_controls["llm_provider"] = llm_provider
            
            # Model Selection based on provider
            model_options = self.llm_options['model_options'][llm_provider.lower()]
            selected_model = st.selectbox(
                "Select Model",
                options=model_options,
                index=0
            )
            self.user_controls["selected_groq_model"] = selected_model
            
            # Temperature Slider
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=self.llm_options['temperature'],
                step=0.1
            )
            self.user_controls["temperature"] = temperature
            
            # Max Tokens Input
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=1,
                max_value=32768,
                value=self.llm_options['max_tokens'],
                step=1
            )
            self.user_controls["max_tokens"] = max_tokens
            
            # Top P Slider
            top_p = st.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=self.llm_options['top_p'],
                step=0.05
            )
            self.user_controls["top_p"] = top_p
            
            # Use Case Selection
            usecase = st.selectbox(
                "Select Use Case",
                options=self.config.get('Default', 'USECASE_OPTIONS', '').split(','),
                index=0
            )
            self.user_controls["usecase"] = usecase
            
            st.divider()
            st.markdown("### About")
            st.markdown("""
            This is an AI-powered application built with LangGraph.
            It provides a flexible interface for interacting with various LLM providers.
            """)
            
    def get_llm(self):
        """Get the appropriate LLM based on user selection."""
        llm_provider = self.user_controls.get("llm_provider", "Groq")
        
        if llm_provider == "Groq":
            return GroqLLM(self.user_controls)
        # Add more LLM providers here as needed
        else:
            st.error(f"LLM provider {llm_provider} not implemented yet.")
            return None
            
    def create_main_interface(self):
        """Create the main chat interface."""
        st.title("🤖 AI Assistant")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
        # Chat input
        if prompt := st.chat_input("What would you like to know?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            # Add AI response to chat history
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Process the message using the provided processor
                    if self.message_processor:
                        response = self.message_processor(prompt)
                    else:
                        # Fallback to direct LLM if no processor is set
                        llm = self.get_llm()
                        if llm:
                            response = llm.generate_response(prompt)
                        else:
                            response = "Unable to initialize LLM. Please check your configuration."
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
    def run(self):
        """Run the Streamlit interface."""
        self.setup_page()
        self.create_sidebar()
        self.create_main_interface()
