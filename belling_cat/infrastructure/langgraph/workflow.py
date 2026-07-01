"""LangGraph workflow for claim investigation."""

from typing import TypedDict

from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from belling_cat.application.services.decomposition_service import DecompositionService
from belling_cat.application.services.investigation_service import InvestigationService
from belling_cat.application.services.verifier_service import VerifierService
from belling_cat.domain.value_objects import Evidence, SubClaim, Verdict


class InvestigationState(TypedDict):
    """State for the investigation workflow."""

    claim: str
    subclaims: list[SubClaim]
    evidence: list[Evidence]
    verdicts: list[Verdict]


def create_workflow(
    decomposition_service: DecompositionService,
    investigation_service: InvestigationService | None = None,
    verifier_service: VerifierService | None = None,
) -> CompiledStateGraph[InvestigationState]:
    """Create the LangGraph workflow for claim investigation.

    Args:
        decomposition_service: Service for decomposing claims into sub-claims
        investigation_service: Optional service for investigating sub-claims
        verifier_service: Optional service for verifying claims and generating verdicts

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
        return {"claim": claim, "subclaims": subclaims, "evidence": [], "verdicts": []}

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
            "verdicts": state.get("verdicts", []),
        }

    def verify_node(state: InvestigationState) -> InvestigationState:
        """Verification node: generates verdicts for sub-claims.

        Args:
            state: Current workflow state

        Returns:
            Updated state with verdicts
        """
        if verifier_service is None:
            return state

        subclaims = state["subclaims"]
        evidence_list = state["evidence"]
        verdicts = []

        # Verify each sub-claim
        for subclaim in subclaims:
            # Filter evidence relevant to this sub-claim
            # For now, use all evidence (in future, could filter by relevance)
            verdict = verifier_service.verify(subclaim, evidence_list)
            verdicts.append(verdict)

        return {
            "claim": state["claim"],
            "subclaims": subclaims,
            "evidence": evidence_list,
            "verdicts": verdicts,
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

        # Add verification node if service provided
        if verifier_service is not None:
            workflow.add_node("verify", verify_node)
            workflow.add_edge("investigate", "verify")
            workflow.add_edge("verify", END)
        else:
            workflow.add_edge("investigate", END)
    else:
        workflow.add_edge("decompose", END)

    # Compile and return
    return workflow.compile()
