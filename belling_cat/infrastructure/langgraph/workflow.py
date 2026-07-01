"""LangGraph workflow for claim investigation."""

from typing import TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from belling_cat.application.services.decomposition_service import DecompositionService
from belling_cat.application.services.investigation_service import InvestigationService
from belling_cat.domain.value_objects import Evidence, SubClaim


class InvestigationState(TypedDict):
    """State for the investigation workflow."""

    claim: str
    subclaims: list[SubClaim]
    evidence: list[Evidence]


def create_workflow(
    decomposition_service: DecompositionService,
    investigation_service: InvestigationService | None = None,
) -> CompiledStateGraph:
    """Create the LangGraph workflow for claim investigation.

    Args:
        decomposition_service: Service for decomposing claims into sub-claims
        investigation_service: Optional service for investigating sub-claims

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
        return {"claim": claim, "subclaims": subclaims, "evidence": []}

    def investigate_node(state: InvestigationState) -> InvestigationState:
        """Investigation node: gathers evidence for sub-claims.

        Args:
            state: Current workflow state

        Returns:
            Updated state with evidence
        """
        if investigation_service is None:
            return state

        subclaims = state["subclaims"]
        all_evidence = []

        # Investigate each sub-claim
        for subclaim in subclaims:
            evidence = investigation_service.investigate(subclaim.text)
            all_evidence.extend(evidence)

        return {
            "claim": state["claim"],
            "subclaims": subclaims,
            "evidence": all_evidence,
        }

    # Build workflow graph
    workflow = StateGraph(InvestigationState)

    # Add nodes
    workflow.add_node("decompose", decompose_node)

    # Set entry point
    workflow.set_entry_point("decompose")

    # Add investigation node if service provided
    if investigation_service is not None:
        workflow.add_node("investigate", investigate_node)
        workflow.add_edge("decompose", "investigate")
        workflow.add_edge("investigate", END)
    else:
        workflow.add_edge("decompose", END)

    # Compile and return
    return workflow.compile()
