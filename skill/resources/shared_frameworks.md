# Shared Decision Frameworks

**These frameworks are available to all templates.**

## First Principles Thinking

When stuck:
1. What's the assumption I'm making?
2. Is it true? (or just conventional wisdom?)
3. What if I invert it?

Example: "Caching always helps" → "When does caching hurt?"

## Simplicity-First

Evaluating options:
1. Does this add ESSENTIAL complexity? (required by problem)
2. Or ACCIDENTAL complexity? (introduced by solution)
ALWAYS prefer less accidental complexity.

## Systems Thinking

Trace ripple effects:
1. What component changes?
2. What depends on it?
3. What depends on those?
4. Are there feedback loops? (amplification?)

## Theory of Constraints

Optimizing:
1. What's the actual bottleneck?
2. Can I optimize AT the bottleneck?
3. What's the NEXT bottleneck after this one?

---

## CKS Availability Check

**Purpose:** Verify Constitutional Knowledge System (CKS) is accessible before querying.

**Usage:** Include this check in any template that needs to query CKS for historical data.

```python
import sys
from pathlib import Path

# Import cross-platform path resolution
from arch.cross_platform_paths import resolve_cks_db_path

# CKS availability check
CKS_AVAILABLE = False
cks_error_msg = None

try:
    # Verify CKS module exists - use cross-platform path resolution
    cks_src_path = resolve_cks_db_path().parent / "src"
    if not cks_src_path.exists():
        raise ImportError(f"CKS source path not found: {cks_src_path}")

    sys.path.insert(0, str(cks_src_path))
    from csf.cks.unified import CKS

    # Verify CKS database exists - use cross-platform path resolution
    cks_db_path = resolve_cks_db_path()
    if not cks_db_path.exists():
        raise FileNotFoundError(f"CKS database not found: {cks_db_path}")

    # Initialize CKS
    cks = CKS(str(cks_db_path))
    CKS_AVAILABLE = True

except (ImportError, FileNotFoundError, Exception) as e:
    cks_error_msg = str(e)
    CKS_AVAILABLE = False
```

**When CKS is NOT available, display:**

```
CKS_UNAVAILABLE_WARNING

Constitutional Knowledge System (CKS) is not accessible:
{cks_error_msg}

Proceeding with generic analysis without CKS historical data.

Recommendation:
1. Verify CKS installation (check cross_platform_paths.resolve_cks_db_path())
2. Ensure CKS source and database paths exist for your platform
3. Consider installing CKS for evidence-based improvements

Continue with generic analysis? [Y/n]
```

**Integration Note:** This code block is referenced by:
- `fast.md` (Stage 1: Query CKS for Failures)
- `deep.md` (Stage 1: Query CKS for Failures)

---

## Codebase-Aware Analysis (Stage 0.3)

**Purpose:** Before making architectural recommendations, read the actual code being discussed. Prevents recommendations that ignore existing patterns, constraints, or complexity.

**When to Activate:** ANY query that references concrete code, files, modules, or subsystems by name.

### Detection

```
codebase_reference_patterns = [
    # Direct file/module references
    r"(?:improve|optimize|redesign|refactor|harden)\s+(?:the\s+)?(\w+(?:\.\w+)*)",
    # Path references
    r"(?:in|at|from)\s+[/\\]?[\w./\\]+\.\w+",
    # Module/class references
    r"(?:the|our|my)\s+(\w+)\s+(?:system|module|service|class|component|hook|pipeline|router)",
]
```

### Protocol

**Step 1: Identify targets**
From the query, extract file/module/system names.

**Step 2: Discover structure**
```
For each identified target:
    1. Glob("**/[target]*") to find matching files
    2. Read top-level files (first 50 lines each, max 5 files)
    3. Extract: imports, class/function signatures, architectural patterns in use
```

**Step 3: Build context summary**
Before proceeding to analysis stages, create an internal context block:

```
CODEBASE CONTEXT:
- Files examined: [list]
- Current patterns: [e.g., "uses asyncio event loop", "hook-based architecture", "singleton CKS instance"]
- Dependencies: [key imports]
- Constraints: [e.g., "Python 3.14", "Windows paths", "no external HTTP calls"]
- Size: [approximate LOC, file count]
```

**Step 4: Carry forward**
This context MUST inform all subsequent stages. Recommendations that contradict discovered patterns must explicitly justify the deviation.

### Skip Conditions

- Query is purely theoretical ("should I use microservices vs monolith")
- Query is about a greenfield project with no existing code
- User says "hypothetical" or "in general"

**Integration Note:** Referenced by all templates at Stage 0.3 (before Domain Inclusion).

---

## Forced Alternative Quality Gate

**Purpose:** Prevent the common failure mode where "3 alternatives" are actually 3 variations of the same idea.

### Distinctiveness Axes

Each alternative MUST differ from every other alternative on at least ONE of these axes:

| Axis | Examples |
|------|----------|
| **Technology choice** | Kafka vs RabbitMQ vs direct HTTP |
| **Data flow direction** | Push vs Pull vs Event-sourced |
| **Deployment model** | Monolith vs Microservices vs Serverless |
| **Consistency model** | Strong vs Eventual vs CRDT |
| **Communication pattern** | Sync vs Async vs Batch |
| **State management** | Stateful vs Stateless vs Externalized |
| **Scaling strategy** | Vertical vs Horizontal vs Sharded |
| **Coupling approach** | Tight integration vs Loose coupling vs Complete isolation |

### Validation Check

After generating alternatives, verify:

```
For each pair (A, B) of alternatives:
    differences = count axes where A and B differ
    if differences == 0:
        REJECT: "Alternatives A and B are not distinct. They differ only in surface details."
        Regenerate B with a genuinely different approach.
```

### Output Format

Each alternative MUST include a **Differs from others on:** line:

```
### Option B: Event-Driven with Message Queue
**Differs from others on:** Communication pattern (async), State management (externalized), Technology (RabbitMQ)
```

**Integration Note:** Referenced by `deep.md` Stage 5, `fast.md` DEFAULT path, `precedent.md` Part 1.

---

## Confidence Calibration Rules

**Purpose:** Tie confidence scores to evidence quality, preventing unjustified high-confidence recommendations.

### Evidence Tiers

| Confidence Range | Required Evidence | Example |
|-----------------|-------------------|---------|
| **90-100%** | Official documentation + production case study from a named organization | "Kafka handles this at LinkedIn scale (source: engineering blog)" |
| **80-89%** | 2+ web sources confirming the recommendation | "Both AWS docs and Confluent recommend this pattern" |
| **70-79%** | 1 web source OR strong CKS historical evidence | "Our CKS shows this pattern succeeded 3 times internally" |
| **60-69%** | Training knowledge only, but pattern is well-established | "Standard microservices decomposition pattern" |
| **40-59%** | Training knowledge, pattern has known trade-offs | "This could work but has documented failure modes" |
| **Below 40%** | Speculative or novel combination | "Untested in production at this scale" |

### Calibration Rules

1. **No unsupported >80%:** Confidence above 80% without web sources triggers: `⚠️ CONFIDENCE ADJUSTMENT: Downgrading from [X]% to [Y]% — no external evidence found to support this confidence level.`

2. **Research-boosted confidence:** If web research found confirming evidence, confidence MAY increase: `📈 Evidence-boosted: [original]% → [new]% based on [source]`

3. **Conflicting evidence penalty:** If sources disagree, cap confidence at 65% and note: `⚠️ CONFLICTING EVIDENCE: Sources disagree on [topic]. Confidence capped.`

4. **Below 60% warning:** Confidence below 60% triggers: `🔍 CONSIDER DEEPER RESEARCH: Low confidence suggests more investigation before committing to this architecture.`

### Output Format

```
## Confidence: 78%

Evidence basis:
- Web: Python 3.13 docs confirm free-threaded mode is experimental [python.org]
- CKS: 2 prior hook system improvements succeeded with this pattern
- Gap: No production case studies for free-threaded Python at scale

Key assumptions:
1. Team has Python 3.13+ available
2. GIL removal won't introduce race conditions in existing code
```

**Integration Note:** Referenced by `deep.md` Stage 10, `fast.md` confidence output, `precedent.md` confidence section.

---

## Version Verification Rule

**Purpose:** Prevent hallucinated version numbers, API signatures, and deprecation claims. LLMs frequently confabulate specific versions.

### Rule

**ANY of the following claims in /arch output MUST be verified by WebFetch against official documentation before inclusion:**

| Claim Type | Examples | Verification Source |
|------------|----------|---------------------|
| **Version numbers** | "FastAPI 0.115", "Python 3.13", "Kafka 3.7" | Official release notes / PyPI / GitHub releases |
| **API signatures** | "asyncio.Runner()", "click.option()" | Official API docs |
| **Deprecation claims** | "get_event_loop() deprecated in 3.12" | PEP or changelog |
| **Feature availability** | "KRaft mode is default since Kafka 3.7" | Official docs |
| **Performance numbers** | "10x faster than X" | Benchmark source |

### Protocol

```
When about to include a specific version/API claim:
    1. Check: Was this verified during Stage 0.7 (Web Research)?
    2. If YES: Include with source citation
    3. If NO: Either
       a) Run a quick WebSearch to verify, OR
       b) Qualify the claim: "As of training data, [claim] — verify current status"
```

### Never Do

- State a specific version number without source
- Claim an API exists/is deprecated without verification
- Quote performance benchmarks from training data without caveat

**Integration Note:** Applies to ALL templates during output generation. Referenced by Web Research Framework.

---

## Template Chaining

**Purpose:** Allow queries that span multiple domains to benefit from multiple template perspectives.

### Detection

```
chain_patterns = [
    # Explicit: "template=python+data-pipeline"
    r"template=(\w+)\+(\w+)",
    # Implicit: query contains keywords from 2+ domains
    # (detected during Stage 1 domain detection when multiple domains match)
]
```

### When Multiple Domains Match

Instead of using "first match in priority order" (current behavior), when 2+ domains have keyword matches:

1. **Primary template:** The domain with the most keyword matches
2. **Secondary template:** The domain with the next most matches
3. **Merge strategy:** Execute primary template fully, then augment with secondary template's domain-specific concerns

### Merge Protocol

```
1. Load primary template
2. Load secondary template's domain-specific sections ONLY:
   - Domain Resource Inclusion items
   - Stage 0.7 research focus areas (merge search queries)
   - Domain-specific anti-patterns / gotchas
3. Do NOT duplicate: prerequisite checks, IMPROVE_SYSTEM/DEFAULT routing, output format
4. Add header: "Analysis combines [primary] + [secondary] domain expertise"
```

### Explicit Override

```
/arch "build Python ETL pipeline" template=python+data-pipeline
```

This loads `python.md` as primary and injects `data-pipeline.md` domain concerns.

### Limits

- Maximum 2 templates chained (3+ creates incoherent output)
- `precedent` template cannot be secondary (it has unique output format)
- `fast` and `deep` are complexity selectors, not chainable domains

**Integration Note:** Referenced by `SKILL.md` Stage 1 (Classify Intent) and Stage 2 (Select Template).

---

## Output Persistence

**Purpose:** Auto-save /arch outputs so they become searchable by CKS for future architecture decisions, creating a feedback loop.

### Storage Location

```
P:/.claude/arch_decisions/
├── YYYY-MM-DD_[template]_[slug].md    # Individual decisions
└── index.jsonl                         # Machine-readable index
```

### Auto-Save Protocol

After the final stage of ANY template execution:

**Step 1: Generate filename**
```python
from datetime import datetime
import re

date = datetime.now().strftime("%Y-%m-%d")
template = selected_template  # e.g., "deep", "fast", "python"
# Slug from first 50 chars of query, sanitized
slug = re.sub(r'[^a-z0-9]+', '-', query[:50].lower()).strip('-')
filename = f"{date}_{template}_{slug}.md"
```

**Step 2: Write decision file**
```markdown
---
date: YYYY-MM-DD
template: [template name]
query: "[original query]"
domain: [detected domain or "generic"]
confidence: [0-100]
research_sources: [list of URLs consulted]
---

[Full /arch output]
```

**Step 3: Append to index**
```jsonl
{"date": "YYYY-MM-DD", "template": "deep", "query": "...", "domain": "python", "confidence": 82, "file": "2026-02-06_deep_improve-hook-system.md"}
```

### CKS Integration

When `/arch` queries CKS during IMPROVE_SYSTEM (Stage 1), it should ALSO search `arch_decisions/index.jsonl` for prior architecture decisions about the same subsystem. This provides:
- What was previously decided and why
- What confidence level the prior decision had
- Whether the prior decision's assumptions still hold

### Skip Conditions

- User says "don't save" or "ephemeral"
- Query was out-of-scope (redirected to another skill)
- Analysis was trivially short (fast template, <2KB output)

**Integration Note:** Referenced by all templates at final output stage.

---

## Adversarial Self-Review (Final Stage)

**Purpose:** After completing the main analysis, systematically challenge the output's weakest points. This is the architectural equivalent of the speculation gate.

### Protocol

After the main analysis is complete but BEFORE presenting to the user:

**Step 1: Identify assumptions**
Re-read the output and list every assumption made (explicit or implicit).

**Step 2: Find the weakest assumption**
Which assumption am I MOST confident about that I HAVEN'T verified? This is the highest-risk blind spot.

**Step 3: Challenge it**
```
For the weakest assumption:
    1. What would happen if this assumption is wrong?
    2. Does the recommendation still hold?
    3. Can I quickly verify it? (WebSearch if possible)
    4. If unverifiable, what's the mitigation?
```

**Step 4: Output**

Add to the end of the analysis:

```
## Adversarial Self-Review

**Weakest assumption:** [the assumption]
**If wrong:** [consequence]
**Mitigation:** [what to do if this turns out to be false]
**Verification status:** [verified by source / unverifiable / partially confirmed]
```

### Review Checklist

| Check | Question |
|-------|----------|
| **Recency bias** | Am I recommending this because it's trendy, or because it's right? |
| **Survivorship bias** | Am I only seeing success stories for this pattern? |
| **Anchoring** | Am I anchored on the first solution that came to mind? |
| **Complexity bias** | Am I recommending something complex because it feels more thorough? |
| **Training data staleness** | Am I citing something that may have changed since training? |

### Skip Conditions

- `fast` template with IMPROVE_SYSTEM path (already CKS-grounded, low risk)
- User explicitly requests speed over thoroughness

**Integration Note:** Referenced by `deep.md` (mandatory), `precedent.md` (mandatory), `fast.md` DEFAULT path (recommended), domain templates (recommended).

**Purpose:** Use WebSearch and WebFetch tools to ground architecture decisions in current best practices, real-world adoption data, and up-to-date library/framework information — rather than relying solely on training data which may be stale.

**When to Research:** ALL architecture queries benefit from research. The depth varies by template:

| Template | Research Depth | Max Searches | Focus |
|----------|---------------|--------------|-------|
| fast | Targeted (1-2 searches) | 3 | Current best practice for the specific pattern/library |
| deep | Comprehensive (3-5 searches) | 8 | Alternatives, trade-offs, real-world post-mortems |
| cli/python/data-pipeline | Domain-focused (2-3 searches) | 5 | Framework versions, breaking changes, migration guides |
| precedent | Evidence-gathering (3-5 searches) | 8 | Industry adoption, case studies, failure reports |

### Research Protocol

**Step 1: Extract Research Queries**

From the user's architecture question, extract 1-5 search queries targeting:

| Query Type | Example | Why |
|------------|---------|-----|
| **Current best practice** | `"[pattern] best practices 2025"` | Training data may reflect outdated consensus |
| **Framework/library status** | `"[library] latest version breaking changes"` | Versions evolve; deprecated APIs cause tech debt |
| **Alternative approaches** | `"[problem] vs [alternative] comparison"` | Forced alternatives are stronger when grounded in real trade-off data |
| **Real-world failures** | `"[pattern] production issues postmortem"` | Pre-mortems are better when informed by actual incidents |
| **Migration/adoption** | `"[technology] migration guide from [old]"` | Realistic effort estimates require real migration stories |

**Step 2: Execute Searches**

```
For each query:
    1. Use WebSearch("[query]") to find relevant results
    2. For the top 1-2 most relevant results, use WebFetch(url) to get full content
    3. Extract: version numbers, trade-offs, gotchas, recommendations
    4. Note the source URL for citation
```

**Step 3: Synthesize into Architecture Context**

Integrate findings into the template's analysis stages. Do NOT dump raw search results. Instead:

- **Cite specific versions** — "FastAPI 0.115+ supports Pydantic v2 natively" not "FastAPI is fast"
- **Cite real trade-offs** — "Team X migrated from monolith to microservices and reported 3x deployment complexity increase (source)" 
- **Cite deprecations/changes** — "asyncio.get_event_loop() is deprecated in Python 3.12+; use asyncio.Runner instead"
- **Flag stale assumptions** — If training data suggests X but research shows the landscape has shifted, explicitly flag it

### Research Skip Conditions

Skip web research ONLY when:
- Query is purely about the user's internal system (IMPROVE_SYSTEM + CKS has data)
- User explicitly says "no research" or "offline"
- Query is about architecture of files/code already loaded in context

### Output Integration

Research findings should appear inline in the template output, not as a separate section. Example:

```
## Stage 5: Forced Alternatives

### Option A: Event-driven with Kafka
- Current status: Kafka 3.7 (Jan 2025) added KRaft mode as default, 
  eliminating ZooKeeper dependency [source: apache.org]
- Adoption: Used by 80%+ of Fortune 100 for event streaming [source: Confluent 2024 report]
- Gotcha: Consumer group rebalancing still causes latency spikes during scaling events
  [source: Uber engineering blog post-mortem]
```

**Integration Note:** This framework is referenced by:
- `fast.md` (Stage 0.7: Research)
- `deep.md` (Stage 0.7: Research / Stage 5: Forced Alternatives)
- All domain templates via shared framework inclusion
