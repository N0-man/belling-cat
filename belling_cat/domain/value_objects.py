"""Domain value objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SubClaim:
    """A discrete, independently verifiable component extracted from a Claim.

    Immutable value object representing a single verifiable fact.
    """

    text: str
