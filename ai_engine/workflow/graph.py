from typing import Any
from langgraph.graph import StateGraph, END
from ai_engine.schemas.pipeline_state import PipelineState
from ai_engine.nodes.validation_node import validation_node

# Stub nodes since they were referenced but not defined
def fix_node(state: Any) -> dict: return {}
def summary_node(state: Any) -> dict: return {}
def sbom_node(state: Any) -> dict: return {}

builder = StateGraph(PipelineState)

# Existing nodes
builder.add_node("fix_node", fix_node)
builder.add_node("summary_node", summary_node)
builder.add_node("sbom_node", sbom_node)

# New validation node
builder.add_node("validation_node", validation_node)

# Edges
builder.add_edge("sbom_node", "validation_node")
builder.add_edge("validation_node", END)

builder.set_entry_point("sbom_node")
graph = builder.compile()