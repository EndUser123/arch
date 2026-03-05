# Python Architecture Analysis

## Template Metadata
- **Target Complexity:** Any
- **Target Domain:** Python 3.12+
- **Expected Output Size:** ~10 KB
- **Execution Instructions:** Read steps, execute in order, do not restate.

## Common Glossary
- **ARCHITECTURE_REVIEW:** Query asks to review/evaluate proposed design or architecture
- **IMPROVE_SYSTEM:** Query asks to optimize/harden existing subsystem
- **DEFAULT:** General architecture decision without improvement intent
- **CKS.db:** Constitutional Knowledge System

## Execution Instructions

**Do not:** Restate these instructions, summarize, or paraphrase.

**Do:**
1. Execute steps sequentially
2. Follow decision tree exactly
3. Python 3.12+ specific analysis (asyncio, type hints, GIL)
4. Stop at each decision point and evaluate

---

## Stage 0: Detect Intent Type

From the user query, identify:

**Is this an ARCHITECTURE_REVIEW request?**
- Keywords: review, evaluate, assess, analyze, audit, validate, critique
- Context: design, architecture, integration, proposal, theoretical
- **If YES:** Proceed to "Stage 0: ARCHITECTURE_REVIEW Path" (below)

**Is this an IMPROVE_SYSTEM request?**
- Keywords: improve, optimize, harden, stabilize, enhance, strengthen
- Subsystem: memory, CKS, hooks, research, retro, lesson, ingestion, validation
- **If YES:** Proceed to "IMPROVE_SYSTEM" below

**Otherwise (DEFAULT):**
- Proceed to "DEFAULT" below

---

## Stage 0: ARCHITECTURE_REVIEW Path

**Purpose**: Evaluate proposed architecture/design WITHOUT recommending alternatives or suggesting implementation first.

### Scope Constraints

**CRITICAL: Architecture reviews are valid EVEN for theoretical/unimplemented designs.**

**DO:**
- Identify gaps and risks in the proposed design
- Evaluate against best practices (from web research in Stage 0.7)
- Assess feasibility and complexity
- Flag missing components or edge cases
- Cite evidence (files, lines, docs) for each finding

**DO NOT:**
- Suggest skipping or delaying the work
- Recommend installation before review
- Propose alternative architectures (that's DEFAULT path)
- Gatekeep based on implementation status
- Declare design "premature" due to lack of installation
- Tell user to "implement first, then review"

### Key Principle

> **Architecture reviews exist PRECISELY to evaluate designs BEFORE implementation.**
> Theoretical designs deserve rigorous analysis precisely to prevent costly mistakes.
> If the design were already implemented, we wouldn't need a review—we'd test it instead.

### Review Stages

1. **Scope Verification** — Confirm understanding of what's being reviewed
2. **Gap Analysis** — Identify missing elements from proposed design
3. **Risk Assessment** — What could fail, based on research + design analysis
4. **Evidence Table** — Each finding MUST be backed by:
   - Specific file:line from codebase (if applicable)
   - Specific line from design document/proposal
   - External source (web research, standards, best practices)

### Output Format

```markdown
## Architecture Review: [Title]

### Scope
[What was reviewed - 1-2 sentences]

### Design Summary
[Brief description of what the design proposes - 2-4 sentences]

### Findings

| ID | Severity | Finding | Evidence | Impact |
|-----|-----------|----------|-----------|---------|
| ARCH-001 | HIGH | [description] | [file:line or source] | [consequence] |
| ARCH-002 | MEDIUM | [description] | [file:line or source] | [consequence] |
| ARCH-003 | LOW | [description] | [file:line or source] | [consequence] |

### Risk Summary
- Technical: [summary]
- Operational: [summary]
- Integration: [summary]

### Conclusion
[Overall assessment - proceed with caution / needs clarification / looks viable with noted gaps]

---
**Confidence:** [X]%

**Evidence basis:**
- Design doc: [source]
- Web research: [count] sources
- Codebase analysis: [files reviewed]

**Key assumptions:**
1. [assumption]
2. [assumption]
```

---

## Stage 0.3: Codebase-Aware Analysis

> See **Codebase-Aware Analysis (Stage 0.3)** in `shared_frameworks.md`.

If query references specific Python files/modules, read them first. Build CODEBASE CONTEXT.

---

## Stage 0.7: Web Research

**Conduct targeted web research before analysis.**

> See **Web Research Framework** in `shared_frameworks.md` for complete protocol.

**For python template: Use Domain-focused depth (2-3 searches, max 5).**

Focus searches on:
1. **Python version features** — New in 3.12/3.13 that affect this pattern (e.g., `asyncio.Runner`, PEP 695 type syntax)
2. **Library/framework status** — Current version, deprecations, migration guides for mentioned libraries
3. **Python-specific trade-offs** — Real benchmarks, GIL-related production experiences, async vs sync comparisons

Integrate findings inline. Cite version numbers and sources.

---

## IMPROVE_SYSTEM

**Trigger:** Query contains "optimize", "harden", "improve", "fix", or targets existing subsystem

### Step 1: Analyze Current State

**Gather evidence about existing system:**
1. What is the current architecture pattern?
2. What are the documented pain points or failures?
3. What metrics or benchmarks exist?
4. What constraints exist (dependencies, platform, team knowledge)?

### Step 2: Identify Python-Specific Issues

Check for common Python anti-patterns:
- **Async misuse:** Using `asyncio` for CPU-bound work
- **GIL contention:** Threading where multiprocessing is needed
- **Type hint gaps:** Missing or imprecise type annotations
- **Resource leaks:** Unclosed resources, missing context managers
- **Framework mismatch:** Wrong web framework for workload

### Step 3: Recommend Improvements

**Provide specific, actionable recommendations:**
- Identify 1-3 highest-impact changes
- Explain Python-specific rationale (asyncio, GIL, typing)
- Estimate effort and risk for each change
- Suggest validation approach (benchmarks, type checking)

### Step 4: Output Format

Use the **Final Output Block** format below.

---

## DEFAULT

**Trigger:** General architecture question without improvement intent

### Step 1: Async Assessment

**Ask:**
- Is this I/O-bound or CPU-bound?
- Does it benefit from asyncio or is sync fine?
- Are there existing async dependencies to coordinate?

**Decision tree:**
- I/O-bound with many concurrent operations → **asyncio**
- CPU-bound with data parallelism → **multiprocessing**
- Simple sequential work → **sync**
- Mixed workload → **hybrid approach**

### Step 2: Type System

**Determine type precision needs:**
- What level of type safety is required?
- Are generics needed for reusable components?
- Should protocols define interfaces?
- Will `@overload` simplify complex APIs?

**Recommend:**
- Basic scripts → Minimal type hints
- Libraries → Protocol-based interfaces
- Applications → Domain models with TypeVars
- Frameworks → Generic with `ParamSpec`

### Step 3: GIL & Multiprocessing

**Assess CPU contention:**
- Is CPU-bound work likely?
- Will multiprocessing add complexity worth the cost?
- Can shared memory be minimized?
- What IPC mechanism is appropriate?

### Step 4: Framework Selection

**Evaluate based on workload:**
- **FastAPI:** Modern async-first, automatic OpenAPI, excellent type hinting
- **Flask:** Lightweight, but consider async alternatives for I/O-heavy
- **Django:** Battery-included, but Django REST Framework adds complexity

### Step 5: Output Format

Use the **Final Output Block** format below.

---

## Output Format

Structure your response using the **Final Output Block** below:

## Final Output Block

**Decision:** [One sentence recommendation]

**Rationale:** [2-3 key reasons, domain-specific]

**Alternatives Considered:** [Brief list with domain trade-offs]
> Apply **Forced Alternative Quality Gate** — each alternative must differ on at least one axis.

**Risk:** [Domain-specific risks]

> Apply **Version Verification Rule** — verify all Python version/API/deprecation claims against official docs.

**Confidence:** [X]% — [evidence basis]
> Apply **Confidence Calibration Rules** from `shared_frameworks.md`.

**Adversarial Self-Review:** (Recommended)
> See **Adversarial Self-Review** in `shared_frameworks.md`. One-line weakest assumption + consequence.

**Persist:** Auto-save to `P:/.claude/arch_decisions/` per **Output Persistence** protocol.

```python
# Filename format (use actual datetime, do not hardcode date)
from datetime import datetime
date = datetime.now().strftime("%Y-%m-%d")
slug = re.sub(r'[^a-z0-9]+', '-', query[:50].lower()).strip('-')
filename = f"{date}_python_{slug}.md"
```

---

## Resilience Considerations

**For Python I/O-bound operations:** Use `@with_resilience(profile='aggressive')` for external API/LLM calls
- Location: `P:/__csf/src/lib/resilience_patterns.py`
- Retry on: `ConnectionError`, `TimeoutError`, `TransientLLMError`, `QuotaError`
- No retry on: `InvalidUserInputError` (user errors should fail fast)

**For async I/O operations:**
```python
from src.lib.resilience_patterns import with_resilience, TransientLLMError

@with_resilience(profile='aggressive', skill_name='my_skill', subagent_name='fetch_agent')
async def fetch_with_retry(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
```

**For write operations (DB, file writes):** Use `@with_resilience(profile='write_path', idempotent=False)`
- Minimal retries (max 1) to avoid duplicate side effects
- Circuit breaker prevents cascade failures

**Feature flags:**
- `RESILIENCE_DISABLED_FOR=<skill_names>` — disable resilience for specific skills
- `RESILIENCE_OBSERVE_ONLY=true` — log without applying resilience patterns

**Observability:**
```python
from src.lib.resilience_patterns import get_resilience_stats
stats = get_resilience_stats('my_skill')  # Filter by skill name
```

---
*End of Python template. Falls back to generic decision format.*
