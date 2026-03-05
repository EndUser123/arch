"""
Architecture decision persistence module.

This module implements the Output Persistence protocol from shared_frameworks.md
for auto-saving /arch outputs to make them searchable by CKS.
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

__all__ = [
    "save_arch_decision",
    "should_skip_persistence",
    "generate_decision_filename",
    "DECISIONS_DIR",
    "INDEX_FILE",
]

# Constants
DECISIONS_DIR = Path(".claude/arch_decisions")
INDEX_FILE = DECISIONS_DIR / "index.jsonl"
MIN_OUTPUT_SIZE_TO_SAVE = 2048  # 2KB minimum output size to save


def should_skip_persistence(
    query: str,
    output: str,
    skip_keywords: tuple[str, ...] = ("don't save", "ephemeral", "do not persist"),
) -> bool:
    """
    Determine if a decision should be skipped from persistence.

    Skip conditions:
    - User says "don't save" or "ephemeral"
    - Query was out-of-scope (redirected to another skill)
    - Analysis was trivially short (fast template, <2KB output)

    Args:
        query: The original user query.
        output: The full /arch output content.
        skip_keywords: Keywords that indicate user wants to skip persistence.

    Returns:
        True if persistence should be skipped, False otherwise.

    Examples:
        >>> should_skip_persistence("don't save this", "...")
        True
        >>> should_skip_persistence("design a system", "x" * 100)
        True
        >>> should_skip_persistence("design a system", "x" * 3000)
        False
    """
    # Check for explicit skip keywords in query
    query_lower = query.lower()
    for keyword in skip_keywords:
        if keyword in query_lower:
            return True

    # Check for trivially short output
    if len(output) < MIN_OUTPUT_SIZE_TO_SAVE:
        return True

    return False


def generate_decision_filename(query: str, template: str) -> str:
    """
    Generate a filename for an architecture decision.

    Filename format: YYYY-MM-DD_[template]_[slug].md

    Args:
        query: The original user query (first 50 chars used for slug).
        template: The template name (e.g., "deep", "fast", "python").

    Returns:
        A filename string.

    Examples:
        >>> generate_decision_filename("design a REST API", "python")
        '2026-02-10_python_design-a-rest-api.md'
    """
    date = datetime.now().strftime("%Y-%m-%d")
    # Slug from first 50 chars of query, sanitized
    slug = re.sub(r"[^a-z0-9]+", "-", query[:50].lower()).strip("-")
    return f"{date}_{template}_{slug}.md"


def save_arch_decision(
    query: str,
    template: str,
    domain: str,
    output: str,
    confidence: int,
    research_sources: Optional[list[str]] = None,
    decisions_dir: Optional[Path] = None,
) -> Optional[str]:
    """
    Save an architecture decision to the arch_decisions/ directory.

    This implements the Output Persistence protocol from shared_frameworks.md.

    Args:
        query: The original user query.
        template: The template name used (e.g., "deep", "fast", "python").
        domain: The detected domain or "generic".
        output: The full /arch output content.
        confidence: Confidence level (0-100).
        research_sources: List of URLs consulted during analysis.
        decisions_dir: Override the default decisions directory path.

    Returns:
        The filepath where the decision was saved, or None if skipped.

    Raises:
        OSError: If unable to create directories or write files.

    Examples:
        >>> save_arch_decision(
        ...     "design a REST API",
        ...     "python",
        ...     "python",
        ...     "Use FastAPI with...",
        ...     85
        ... )
        '.claude/arch_decisions/2026-02-10_python_design-a-rest-api.md'
    """
    # Check skip conditions
    if should_skip_persistence(query, output):
        return None

    # Use provided directory or default
    if decisions_dir is None:
        decisions_dir = DECISIONS_DIR

    # Create directory if it doesn't exist
    decisions_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename
    filename = generate_decision_filename(query, template)
    filepath = decisions_dir / filename

    # Format research sources for frontmatter
    if research_sources is None:
        research_sources = []
    sources_str = json.dumps(research_sources)

    # Build YAML frontmatter
    date = datetime.now().strftime("%Y-%m-%d")
    frontmatter = f"""---
date: {date}
template: {template}
query: "{query}"
domain: {domain}
confidence: {confidence}
research_sources: {sources_str}
---

{output}
"""

    # Write decision file
    filepath.write_text(frontmatter, encoding="utf-8")

    # Append to index.jsonl
    index_entry = {
        "date": date,
        "template": template,
        "query": query,
        "domain": domain,
        "confidence": confidence,
        "file": filename,
    }

    # Use the same decisions_dir for index file
    index_path = decisions_dir / "index.jsonl"
    with open(index_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(index_entry) + "\n")

    return str(filepath)


def load_decision_index(index_path: Optional[Path] = None) -> list[dict[str, Any]]:
    """
    Load the architecture decision index.

    Args:
        index_path: Override the default index file path.

    Returns:
        A list of decision index entries.

    Raises:
        FileNotFoundError: If index file doesn't exist.
        json.JSONDecodeError: If index file contains invalid JSON.
    """
    if index_path is None:
        index_path = INDEX_FILE

    decisions = []
    with open(index_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                decisions.append(json.loads(line))

    return decisions


def search_decisions(
    query: str,
    index_path: Optional[Path] = None,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """
    Search prior architecture decisions by query keywords.

    This provides CKS integration for searching prior decisions.

    Args:
        query: Search query string.
        index_path: Override the default index file path.
        limit: Maximum number of results to return.

    Returns:
        A list of matching decision entries.

    Examples:
        >>> search_decisions("hook system")
        [{'date': '2026-02-06', 'template': 'deep', 'query': '...', ...}]
    """
    try:
        decisions = load_decision_index(index_path)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    # Simple keyword matching (could be enhanced with proper search)
    query_lower = query.lower()
    query_words = set(query_lower.split())

    scored = []
    for decision in decisions:
        # Search in query and domain fields
        searchable_text = (
            f"{decision.get('query', '')} {decision.get('domain', '')}".lower()
        )
        score = sum(1 for word in query_words if word in searchable_text)
        if score > 0:
            scored.append((score, decision))

    # Sort by score descending and return top results
    scored.sort(key=lambda x: x[0], reverse=True)
    return [decision for _, decision in scored[:limit]]
