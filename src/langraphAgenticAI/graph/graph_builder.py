from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from langchain_core.prompts import ChatMessagePromptTemplate
from src.langraphAgenticAI.state.state import AgentState
from src.langraphAgenticAI.nodes.basic_chatbot_node import BasicChatBot


class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        
    def basic_chatbot_build_graph(self):
        """
        Build a basic LangGraph chatbot graph.
        
        Returns:
            StateGraph: A compiled LangGraph state graph.
        """
        # Create a state graph with the defined state
        graph = StateGraph(AgentState)
        
        # Create the basic chatbot node
        chatbot_node = BasicChatBot(self.llm)
        
        # Add the chatbot node to the graph
        graph.add_node("chatbot", chatbot_node.run)
        
        # Set the entry point for the graph
        graph.set_entry_point("chatbot")
        
        # Add conditional edges
        graph.add_conditional_edges(
            "chatbot",
            # For now, we're just ending after one response
            lambda state: END
        )
        
        # Compile the graph
        compiled_graph = graph.compile()
        
        return compiled_graph
    
    def tool_using_chatbot_build_graph(self, tools=None):
        """
        Build a LangGraph chatbot with tools.
        
        Args:
            tools (list): List of tools the chatbot can use.
            
        Returns:
            StateGraph: A compiled LangGraph state graph with tools.
        """
        if not tools:
            tools = []
            
        # Create a state graph with the defined state
        graph = StateGraph(AgentState)
        
        # Create the basic chatbot node
        chatbot_node = BasicChatBot(self.llm, tools=tools)
        
        # Create a tool node
        tool_node = ToolNode(tools)
        
        # Add the chatbot node to the graph
        graph.add_node("chatbot", chatbot_node.run)
        
        # Add the tool node to the graph
        graph.add_node("tools", tool_node)
        
        # Set the entry point for the graph
        graph.set_entry_point("chatbot")
        
        # Add conditional edges
        graph.add_conditional_edges(
            "chatbot",
            tools_condition,
            {
                "tools": "tools",
                END: END
            }
        )
        
        # Add edge from tools back to chatbot
        graph.add_edge("tools", "chatbot")
        
        # Compile the graph
        compiled_graph = graph.compile()
        
        return compiled_graph