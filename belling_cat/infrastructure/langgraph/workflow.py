"""LangGraph workflow for claim investigation."""

from typing import TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from belling_cat.application.services.decomposition_service import DecompositionService
from belling_cat.domain.value_objects import SubClaim


class InvestigationState(TypedDict):
    """State for the investigation workflow."""

    claim: str
    subclaims: list[SubClaim]


def create_workflow(decomposition_service: DecompositionService) -> CompiledStateGraph:
    """Create the LangGraph workflow for claim investigation.

    Args:
        decomposition_service: Service for decomposing claims into sub-claims

    Returns:
        Compiled LangGraph workflow
    """

    def decompose_node(state: InvestigationState) -> InvestigationState:
        """Decomposition node: breaks claim into sub-claims.

        Args:
            state: Current workflow state

        Returns:
            Updated state with sub-claims
        """
        claim = state["claim"]
        subclaims = decomposition_service.decompose(claim)
        return {"claim": claim, "subclaims": subclaims}

    # Build workflow graph
    workflow = StateGraph(InvestigationState)

    # Add nodes
    workflow.add_node("decompose", decompose_node)

    # Set entry point
    workflow.set_entry_point("decompose")

    # Add edges
    workflow.add_edge("decompose", END)

    # Compile and return
    return workflow.compile()
