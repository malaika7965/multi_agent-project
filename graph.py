from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.router_agent import RouterAgent
from agents.rag_agent import RAGAgent
from agents.general_agent import GeneralAgent
from agents.evaluator_agent import EvaluatorAgent
from tools.rag_tool import UniversityWebTool

class AgentState(TypedDict):
    user_query: str
    query_type: str
    retrieved_context: str
    agent_response: str
    evaluation_result: str

# Instances
router = RouterAgent()
rag_agent = RAGAgent()
general_agent = GeneralAgent()
evaluator = EvaluatorAgent()
web_tool = UniversityWebTool()

# Nodes logic
def router_node(state: AgentState):
    return {"query_type": router.classify(state["user_query"])}

def rag_node(state: AgentState):
    context = web_tool.search_university_data(state["user_query"])
    response = rag_agent.generate_answer(state["user_query"], context)
    return {"retrieved_context": context, "agent_response": response}

def general_node(state: AgentState):
    response = general_agent.handle_chat(state["user_query"])
    return {"agent_response": response}

def evaluator_node(state: AgentState):
    result = evaluator.evaluate(state["user_query"], state["agent_response"])
    return {"evaluation_result": result}

# Graph setup
workflow = StateGraph(AgentState)
workflow.add_node("router", router_node)
workflow.add_node("rag_agent", rag_node)
workflow.add_node("general_agent", general_node)
workflow.add_node("evaluator", evaluator_node)

workflow.set_entry_point("router")

def route_after_classification(state: AgentState):
    return "rag_agent" if state["query_type"] == "university_info" else "general_agent"

workflow.add_conditional_edges("router", route_after_classification, {"rag_agent": "rag_agent", "general_agent": "general_agent"})
workflow.add_edge("rag_agent", "evaluator")
workflow.add_edge("general_agent", "evaluator")

def route_after_evaluation(state: AgentState):
    return END if "pass" in state["evaluation_result"] else "general_agent"

workflow.add_conditional_edges("evaluator", route_after_evaluation, {END: END, "general_agent": "general_agent"})

compiled_graph = workflow.compile()