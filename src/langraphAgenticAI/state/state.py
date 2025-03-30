from typing import Dict, List, Any, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import MessagesState


class AgentState(MessagesState):
    """
    State class for the agent, extending the MessagesState from LangGraph.
    
    Attributes:
        messages (List[BaseMessage]): The list of messages in the conversation.
        tool_calls (List[Dict]): The list of tool calls made by the agent.
        tool_responses (Dict[str, Any]): The responses to tool calls.
        metadata (Dict[str, Any]): Additional metadata for the agent.
    """
    
    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """
        Get the LangChain namespace for serialization.
        
        Returns:
            List[str]: List of namespace components.
        """
        return ["langraphAgenticAI", "state"]

    
    def __init__(
        self,
        messages: Optional[List[BaseMessage]] = None,
        tool_calls: Optional[List[Dict]] = None,
        tool_responses: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the state with messages, tool calls, responses, and metadata.
        
        Args:
            messages: The conversation messages.
            tool_calls: Any tool calls made by the agent.
            tool_responses: Responses from tools.
            metadata: Additional metadata.
        """
        super().__init__(messages=messages or [])
        self.tool_calls = tool_calls or []
        self.tool_responses = tool_responses or {}
        self.metadata = metadata or {}
