from typing import Dict, List, Tuple, Optional, Any
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool

class BasicChatBot:
    """
    A basic chatbot node for LangGraph.
    
    This node handles the conversation with the user and generates responses
    using the specified LLM.
    """
    
    def __init__(self, llm, tools=None):
        """
        Initialize the basic chatbot node.
        
        Args:
            llm: The language model to use for generating responses.
            tools (Optional[List[BaseTool]]): List of tools the chatbot can use.
        """
        self.llm = llm
        self.tools = tools or []
        
        # Set up the prompt template
        self._setup_prompt()
    
    def _setup_prompt(self):
        """Set up the prompt template for the chatbot."""
        template = """You are a helpful AI assistant built with LangGraph.
        
Your goal is to provide useful, accurate, and friendly responses to the user's questions.

{chat_history}

User: {input}"""

        if self.tools:
            # If tools are available, add tool instructions
            tool_names = [tool.name for tool in self.tools]
            tool_descs = [f"{tool.name}: {tool.description}" for tool in self.tools]
            
            # Add tool instructions to the prompt
            template += f"""

You have access to the following tools:
{tool_descs}

To use a tool, please use the following format:
Action: the action to take, should be one of {tool_names}
Action Input: the input to the action
Observation: the result of the action

When you have a response to say to the human, or if you don't need to use a tool, you MUST use the format:
Thought: I now know the final answer
Final Answer: [your response here]"""
        
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
    def run(self, state):
        """
        Run the chatbot node on the given state.
        
        Args:
            state: The current state of the conversation.
            
        Returns:
            dict: The updated state after generating a response.
        """
        # Extract the input from the last human message
        human_messages = [msg for msg in state.messages if isinstance(msg, HumanMessage)]
        if not human_messages:
            return state
        
        last_human_msg = human_messages[-1].content
        
        # Prepare chat history (all messages except the last human message)
        chat_history = state.messages[:-1] if state.messages else []
        
        # Get previous AI and human messages for the prompt
        chain = self.prompt | self.llm
        
        # Generate response
        response = chain.invoke({
            "chat_history": chat_history,
            "input": last_human_msg
        })
        
        # Update the state with the AI's response
        state.messages.append(AIMessage(content=response.content))
        
        return state 