"""Domain value objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SubClaim:
    """A discrete, independently verifiable component extracted from a Claim.

    Immutable value object representing a single verifiable fact.
    """

    text: str


@dataclass(frozen=True)
class Source:
    """An information origin with credibility attributes.

    Authority hierarchy: government > academic > established news > other.
    """

    url: str
    authority_level: str
    publication_date: str


@dataclass(frozen=True)
class Evidence:
    """A sourced fact discovered during investigation.

    Includes the content, source reference, credibility assessment, and timestamp.
    """

    source: Source
    quote: str
    timestamp: str  # ISO 8601 format


@dataclass(frozen=True)
class Finding:
    """An intermediate discovery or progress update during investigation.

    Immutable records streamed to the user in real-time.
    """

    message: str
