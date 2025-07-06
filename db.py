"""
Database of publications and other structured data for the website.
"""
# ruff: noqa: E501

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Paper:
    """Represents a single academic paper/publication."""

    title: str
    authors: str
    year: int
    venue: str
    urls: Optional[Dict[str, str]] = None
    description: Optional[str] = None


PAPERS = [
    Paper(
        title=(
            "POSGGym: A Library for Decision-Theoretic Planning and Learning "
            "in Partially Observable, Multi-Agent Environments"
        ),
        authors="Jonathon Schwartz, Rhys Newbury, Dana Kulic, Hanna Kurniawati",
        year=2024,
        venue="ICAPS Workshop on Planning and Reinforcement Learning",
        urls={
            "paper": "https://icaps24.icaps-conference.org/program/workshops/prl-papers/17.pdf",
            "code": "https://github.com/RDLLab/posggym",
        },
    ),
    Paper(
        title=(
            "Combining a Meta-Policy and Monte-Carlo Planning for Scalable "
            "Type-Based Reasoning in Partially Observable Environments"
        ),
        authors="Jonathon Schwartz, Hanna Kurniawati, Marcus Hutter",
        year=2023,
        venue="arXiv preprint",
        urls={
            "paper": "https://arxiv.org/pdf/2306.06067",
        },
    ),
    Paper(
        title="Online Planning for Interactive-POMDPs using Nested Monte Carlo Tree Search",
        authors="Jonathon Schwartz, Ruijia Zhou, Hanna Kurniawati",
        year=2022,
        venue=("International Conference on Intelligent Robots and Systems (IROS)"),
        urls={
            "paper": "https://rdl.cecs.anu.edu.au/papers/iros22_ntmcp.pdf",
        },
    ),
    Paper(
        title="POMDP+ Information-Decay: Incorporating Defender's Behaviour in Autonomous Penetration Testing",
        authors="Jonathon Schwartz, Hanna Kurniawati, Edwin El-Mahassni",
        year=2020,
        venue=("International Conference on Automated Planning and Scheduling (ICAPS)"),
        urls={
            "paper": "https://aaai.org/ojs/index.php/ICAPS/article/download/6666/6520/",
        },
    ),
    Paper(
        title="CybORG: An Autonomous Cyber Operations Research Gym",
        authors=(
            "Callum Baillie, Maxwell Standen, Jonathon Schwartz, "
            "Michael Docking, David Bowman, Junae Kim"
        ),
        year=2020,
        venue="arXiv preprint",
        urls={
            "paper": "https://arxiv.org/pdf/2002.10667",
        },
    ),
    Paper(
        title="Autonomous Penetration Testing using Reinforcement Learning",
        authors="Jonathon Schwartz, Hanna Kurniawati",
        year=2019,
        venue="arXiv preprint",
        urls={
            "paper": "https://arxiv.org/pdf/1905.05965",
        },
    ),
]
