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
    venue: str | None
    urls: Optional[Dict[str, str]] = None
    description: Optional[str] = None


@dataclass
class Project:
    """Represents an open source project."""

    title: str
    description: str
    url: str

MY_NAME = "Jonathon Schwartz"


PAPERS = [
    Paper(
        title="Towards Scalable Planning in Partially Observable, Multi-Agent Environments",
        authors=f"{MY_NAME}",
        year=2025,
        venue="PhD Thesis",
        urls={
            # TODO add link to thesis once it's published
            "thesis (coming soon)": "coming soon",
        },
    ),
    Paper(
        title="POSGGym: A Library for Decision-Theoretic Planning and Learning in Partially Observable, Multi-Agent Environments",
        authors=f"{MY_NAME}, Rhys Newbury, Dana Kulić, Hanna Kurniawati",
        year=2025,
        venue="Journal of Autonomous Agents and Multi-Agent Systems (JAAMAS)",
        urls={
            # TODO add link to journalpaper once it's published
            "paper (coming soon)": "coming soon",
            "workshop paper (ICAPS PRL workshop '24)": "https://icaps24.icaps-conference.org/program/workshops/prl-papers/17.pdf",
            "code": "https://github.com/RDLLab/posggym",
        },
    ),
    Paper(
        title="Combining a Meta-Policy and Monte-Carlo Planning for Scalable Type-Based Reasoning in Partially Observable Environments",
        authors=f"{MY_NAME}, Hanna Kurniawati, Marcus Hutter",
        year=2023,
        venue="International Conference on Autonomous Agents and Multiagent Systems (AAMAS)",
        urls={
            "paper": "https://arxiv.org/pdf/2306.06067",
            "extended abstract version": "https://www.ifaamas.org/Proceedings/aamas2023/pdfs/p2355.pdf",
            "code": "https://github.com/Jjschwartz/potmmcp"
        },
    ),
    Paper(
        title="Online Planning for Interactive-POMDPs using Nested Monte Carlo Tree Search",
        authors=f"{MY_NAME}, Ruijia Zhou, Hanna Kurniawati",
        year=2022,
        venue="International Conference on Intelligent Robots and Systems (IROS)",
        urls={
            "paper": "https://rdl.cecs.anu.edu.au/papers/iros22_ntmcp.pdf",
            "code": "https://github.com/RDLLab/i-ntmcp"
        },
    ),
    Paper(
        title="POMDP+ Information-Decay: Incorporating Defender's Behaviour in Autonomous Penetration Testing",
        authors=f"{MY_NAME}, Hanna Kurniawati, Edwin El-Mahassni",
        year=2020,
        venue="International Conference on Automated Planning and Scheduling (ICAPS)",
        urls={
            "paper": "https://aaai.org/ojs/index.php/ICAPS/article/download/6666/6520/",
        },
    ),
    Paper(
        title="CybORG: An Autonomous Cyber Operations Research Gym",
        authors=f"Callum Baillie, Maxwell Standen, {MY_NAME}, Michael Docking, David Bowman, Junae Kim",
        year=2020,
        venue="arXiv preprint",
        urls={
            "paper": "https://arxiv.org/pdf/2002.10667",
            "extension (IJCAI '21)": "https://arxiv.org/pdf/2108.09118",
            "code": "https://github.com/cage-challenge/CybORG",
        },
    ),
    Paper(
        title="Autonomous Penetration Testing using Reinforcement Learning",
        authors=f"{MY_NAME}",
        year=2019,
        venue="Undergraduate Thesis",
        urls={
            "thesis": "https://arxiv.org/pdf/1905.05965",
            "code": "https://github.com/Jjschwartz/NetworkAttackSimulator",
        },
    ),
]


PROJECTS = [
    Project(
        title="POSGGym",
        description=(
            "A collection of environments and reference agents for planning and reinforcement learning research in partially observable, multi-agent environments. "
            "Related to this is also <a href='https://github.com/RDLLab/posggym-baselines' target='_blank'>POSGGym-Baselines</a> which contains baseline "
            "implementations of planning and reinforcement learning algorithms for POSGGym environments."
        ),
        url="https://github.com/RDLLab/posggym"
    ),
    Project(
        title="Network Attack Simulator",
        description=(
            "Reinforcement learning environment for training autonomous network penetration testing agents. "
            "Simulates attack scenarios involving different network topologies vulnerabilities, scans, and exploits."
        ),
        url="https://github.com/Jjschwartz/NetworkAttackSimulator"
    ),
    Project(
        title="miniDRL",
        description=(
            "Minimal implementations of distributed, recurrent, deep reinforcement learning algorithms (PPO, R2D2). "
            "Distributed RL, especially recurrent RL, gets pretty complex fast, this project contains some easy-to-follow stand-alone implementations of some distributed RL algorithms."
        ),
        url="https://github.com/Jjschwartz/miniDRL"
    ),
]
