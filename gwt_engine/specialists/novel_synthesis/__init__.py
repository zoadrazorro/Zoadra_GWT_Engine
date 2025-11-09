"""
Novel Philosophical Synthesis System
======================================

A comprehensive system for generating genuinely original philosophical frameworks
by integrating multi-domain knowledge, adversarial dialectics, empirical validation,
meta-philosophical analysis, and dialectical synthesis.

Components:
- multi_domain_ingestion: Ingest knowledge from beyond philosophy
- adversarial_dialectic: Generate thesis/antithesis/synthesis
- empirical_validation: Test claims against empirical evidence
- meta_philosophical_analyzer: Analyze system's own outputs for biases
- dialectical_twins: Universalis vs Metaluminosity debate system
"""

from .multi_domain_ingestion import (
    MultiDomainKnowledgeBase,
    GapIdentifier,
    DomainType,
    DomainKnowledge,
    PhilosophicalGap
)

from .adversarial_dialectic import (
    AdversarialDialectic,
    PhilosophicalPosition,
    Argument,
    DialecticalSynthesis,
    ArgumentStrength
)

from .empirical_validation import (
    EmpiricalValidator,
    EmpiricalClaim,
    EmpiricalEvidence,
    ValidationReport,
    ValidationResult
)

from .meta_philosophical_analyzer import (
    MetaPhilosophicalAnalyzer,
    OutputPattern,
    IdentifiedBias,
    BlindSpot,
    SelfAnalysisReport
)

from .dialectical_twins import (
    DialecticalTwinSystem,
    PhilosophicalSystem,
    DialecticalExchange,
    TranscendentSynthesis,
    ETHICA_UNIVERSALIS,
    ETHICA_METALUMINOSA
)

__all__ = [
    # Multi-domain ingestion
    "MultiDomainKnowledgeBase",
    "GapIdentifier",
    "DomainType",
    "DomainKnowledge",
    "PhilosophicalGap",

    # Adversarial dialectic
    "AdversarialDialectic",
    "PhilosophicalPosition",
    "Argument",
    "DialecticalSynthesis",
    "ArgumentStrength",

    # Empirical validation
    "EmpiricalValidator",
    "EmpiricalClaim",
    "EmpiricalEvidence",
    "ValidationReport",
    "ValidationResult",

    # Meta-analysis
    "MetaPhilosophicalAnalyzer",
    "OutputPattern",
    "IdentifiedBias",
    "BlindSpot",
    "SelfAnalysisReport",

    # Dialectical twins
    "DialecticalTwinSystem",
    "PhilosophicalSystem",
    "DialecticalExchange",
    "TranscendentSynthesis",
    "ETHICA_UNIVERSALIS",
    "ETHICA_METALUMINOSA",
]
