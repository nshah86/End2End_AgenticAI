import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class GroqLLM:
    def __init__(self, user_controls_input):
        self.user_controls_input = user_controls_input

    def get_llm_model(self):
        try:
            groq_api_key = self.user_controls_input.get('GROQ_API_KEY', os.environ.get('GROQ_API_KEY', ''))
            selected_groq_model = self.user_controls_input.get('selected_groq_model', 'mixtral-8x7b-32768')
            temperature = float(self.user_controls_input.get('temperature', 0.7))
            max_tokens = int(self.user_controls_input.get('max_tokens', 4096))
            
            # Check if API key is provided
            if not groq_api_key:
                raise ValueError("Groq API key is required. Please provide it in the configuration.")
            
            # Initialize the Groq LLM
            llm = ChatGroq(
                groq_api_key=groq_api_key,
                model_name=selected_groq_model,
                temperature=temperature,
                max_tokens=max_tokens,
                streaming=True,
                callbacks=[StreamingStdOutCallbackHandler()]
            )
            
            return llm
        
        except Exception as e:
            st.error(f"Error initializing Groq LLM: {str(e)}")
            return None
    
    def generate_response(self, prompt):
        """
        Generate a response using the Groq LLM.
        
        Args:
            prompt (str): The user prompt to generate a response for.
            
        Returns:
            str: The generated response from the LLM.
        """
        try:
            llm = self.get_llm_model()
            if llm:
                response = llm.invoke(prompt)
                return response.content
            else:
                return "Error: Unable to initialize LLM model. Please check your API key and configuration."
        
        except Exception as e:
            return f"Error generating response: {str(e)}"