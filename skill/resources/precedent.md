# ADR Documentation Analysis

## Template Metadata
- **Target Complexity:** Any
- **Target Domain:** Architectural Decision Records
- **Expected Output Size:** ~20 KB
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
3. ADR-specific analysis (documenting decisions, alternatives)
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
- **If YES:** This template may not apply - use appropriate domain template

**Otherwise (DEFAULT):**
- Proceed to "ADR Documentation Analysis" below

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

# Architectural Decision Record

**Purpose:** Comprehensive analysis with permanent documentation for precedent-setting decisions.

## Stage 0.7: Web Research

**Before analysis, conduct evidence-gathering web research.**

> See **Web Research Framework** in `shared_frameworks.md` for complete protocol.

**For precedent template: Use Evidence-gathering depth (3-5 searches, max 8).**

Focus searches on:
1. **Industry adoption** — How widely is this pattern/technology adopted? By whom?
2. **Case studies** — Who has done this before? What were their outcomes?
3. **Failure reports** — What are documented failures with this approach?
4. **Standards/RFCs** — Are there industry standards or emerging RFCs relevant to this decision?

Research is especially critical for ADRs since these are permanent records. Cite sources in ADR document.

## Stage 0.3: Codebase-Aware Analysis

> See **Codebase-Aware Analysis (Stage 0.3)** in `shared_frameworks.md`.

If decision concerns existing code, read it first. Build CODEBASE CONTEXT block before analysis.

## When to Use

Use this for decisions that:
- Set long-term precedent (6+ months)
- Require team-wide or historical awareness
- Schema redesigns or breaking API changes
- New service boundaries or architectural foundations
- Strategic architectural choices

## Process

### Part 1: Comprehensive Analysis (40-90 min)

Full analysis following `/arch-deep` stages:
1. Complexity verification
2. Mental model (grounded in research)
3. Pre-mortem (informed by real failure data)
4. Risk matrix
5. Alternatives — **apply Forced Alternative Quality Gate** (see `shared_frameworks.md`)
6. Rollback plan
7. Technical debt
8. Timeline
9. Implementation checklist
10. Confidence — **apply Confidence Calibration Rules** (see `shared_frameworks.md`)
11. Adversarial self-review (MANDATORY — see `shared_frameworks.md`)

> **Version Verification Rule** applies throughout — verify all version/API claims (see `shared_frameworks.md`).

### Part 2: Record Decision (20+ min)

After analysis, offer three documentation options:

**Option 1: Draft ADR** (Architecture Decision Record)
- Saved to `P:/adr/ADR-XXXX-<slug>.md`
- Versioned, searchable, linkable from code
- Use for: Breaking changes, schema migrations, major patterns

**Option 2: Generate Documentation**
- System architecture overview
- Module inventory and data flows
- Onboarding guide with key decisions
- Use for: Cleaning up docs, new team members

**Option 3: Archive Decision**
- Full markdown dump of analysis to repository
- Historical record for future reference
- Use for: Precedent tracking, decision history

### Part 3: Persist Output

> See **Output Persistence** in `shared_frameworks.md`.

Auto-save to `P:/.claude/arch_decisions/` with metadata. ADR decisions are ALWAYS persisted (never skip).

```python
# Filename format (use actual datetime, do not hardcode date)
from datetime import datetime
date = datetime.now().strftime("%Y-%m-%d")
slug = re.sub(r'[^a-z0-9]+', '-', query[:50].lower()).strip('-')
filename = f"{date}_precedent_{slug}.md"
```

## ADR Template

```markdown
# ADR-XXXX: [Short Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Superseded
**Context:** What situation prompted this decision

## Decision
What was decided.

## Rationale
Why this is right. What patterns apply.

## Consequences
- Good: Benefits
- Bad: Costs, risks, tradeoffs

## Alternatives Considered
- Alternative A: Reason not chosen
- Alternative B: Reason not chosen

## Related Decisions
- ADR-XXXX: Related precedent (if any)
```

## Success Criteria

Full analysis complete (all 11 stages)
ADR is clear and concise (1-2 pages)
Decision justified with consequences
Alternatives explored and rejected with reasoning
Saved to version control
Linkable from relevant code

---

## Resilience Considerations

**For precedent-setting architectural decisions:** Consider documenting resilience requirements
- Location: `P:/__csf/src/lib/resilience_patterns.py`
- Retry on: `ConnectionError`, `TimeoutError`, `TransientLLMError`, `QuotaError`
- No retry on: `InvalidUserInputError` (user errors should fail fast)

**When ADR involves external service dependencies:**
- Document whether service is called with `@with_resilience` decorator
- Specify profile: `conservative`, `aggressive`, `read_only`, or `write_path`
- Note idempotency requirements for write operations

**Example ADR resilience clause:**
```markdown
## Resilience Requirements
- External API calls: Use `@with_resilience(profile='aggressive', idempotent=True)`
- Database writes: Use `@with_resilience(profile='write_path', idempotent=False)`
- Circuit breaker threshold: 5 consecutive failures opens circuit
- Feature flag: `RESILIENCE_DISABLED_FOR=my_feature` for graceful degradation
```

**Feature flags:**
- `RESILIENCE_DISABLED_FOR=<skill_names>` — disable resilience for specific features
- `RESILIENCE_OBSERVE_ONLY=true` — log without applying resilience patterns

**Import:**
```python
from src.lib.resilience_patterns import with_resilience, TransientLLMError, QuotaError
```
