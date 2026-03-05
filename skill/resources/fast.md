# Quick Architecture Decision

## Template Metadata
- **Target Complexity:** LOW
- **Target Domain:** Generic
- **Expected Output Size:** ~5 KB
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
3. Keep outputs focused unless user requests depth
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
- **If YES:** Proceed to "Stage 0.5: Prerequisite Check" below

**Otherwise (DEFAULT):**
- Proceed to "Stage 0.5: Prerequisite Check" below

---

## Stage 0: ARCHITECTURE_REVIEW Path

**Purpose**: Evaluate proposed architecture/design WITHOUT recommending alternatives or suggesting implementation first.

### Role Assignment

**Before review begins, adopt this role:**

```
"Act as a Senior Architecture Reviewer for this task.

Your scope: Review ONLY proposed designs.
Do NOT suggest alternatives or recommend installation before review.
Output ONLY issues in table format: ID | Severity | Evidence (file:line) | Impact"
```

> **Note:** "Act as" is task-bound and less likely to persist across turns than "You are".
> Reduces off-topic advice by 50-70% (source: external prompting research).

### Few-Shot Examples

**Before user's review, show expected format:**

```
Example 1:
Code: `cache = {}  # global`
Review: MEDIUM: Global state risk. Evidence: Line 1. Impact: Threading issues in concurrent access.

Example 2:
Code: `def federate_query(backend): return backend.query()`
Review: HIGH: No failure handling. Evidence: Line 1 lacks fallback. Impact: Partial results on timeout.
```

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

### Review Stages (Graph-of-Thoughts Inspired)

1. **Scope Verification** — Confirm understanding of what's being reviewed
2. **Gap Analysis** — Identify missing elements from proposed design
3. **Risk Assessment** — What could fail, based on research + design analysis
4. **Structured Analysis** — Model architecture as interconnected nodes for deeper insight
5. **Evidence Table** — Each finding MUST be backed by:
   - Specific file:line from codebase (if applicable)
   - Specific line from design document/proposal
   - External source (web research, standards, best practices)

### Structured Analysis Steps (Optional for Complex Reviews)

For multi-system or complex integration reviews, use graph-based reasoning:

```
Step 1: Generate Architecture Nodes
- Node A: "Federated query architecture"
- Node B: "Checkpoint integration"
- Node C: "claude-mem integration"

Step 2: Generate Edge Relationships
- A → B: "A depends on B for query federation"
- A → C: "A shares state with C via session handoff"

Step 3: Aggregate Findings
- Merge related concerns into synthesis nodes
- Identify cross-cutting risks

Step 4: Refine Output
- Converge graph-based analysis into final review format
- Preserve traceability of reasoning path
```

**Note:** This GoT-style approach is optional. Use for complex multi-system reviews when simple linear analysis is insufficient.

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

## Stage 0.5: Prerequisite Check

**Semantic analysis for prerequisite detection:**

Before proceeding with architectural analysis, analyze query for semantic patterns that suggest another workflow should run first.

### Prerequisite Detection Table

| Pattern | Detected When (semantic analysis) | Suggest | Rationale |
|---------|-----------------------------------|---------|-----------|
| Missing requirements | Query mentions PRD, spec, requirements, "from requirements", no specs loaded | `/prd "<requirement_source>"` | Architecture needs requirements foundation |
| Unknown codebase | First-time context, "how is X structured", no prior file reads | `/discover "<area>"` | Need codebase understanding before design |
| Debug/diagnosis focus | "why failing", "broken", "error", "crash", "bug in" | `/debug "<issue>"` or `/rca "<issue>"` | Diagnosis before architecture |
| Planning phase | "how to build", "steps for", "plan to implement", "implementation approach" | `/plan "<feature>"` or `/breakdown "<task>"` | Planning precedes architecture |
| Verification focus | "verify", "check my work", "is this correct", "did I implement right" | `/verify "<target>"` | Verification before redesign |
| Research needed | "how does X work", "learn about", "understand", "research" | `/research "<topic>"` | Understanding before decisions |
| Deployment/ship | "deploy", "ship", "release", "production ready" | `/qa` (QA certification) | QA before deployment |

### If Prerequisite Detected

```
┌─────────────────────────────────────────────────────────────┐
│ 🔔 PREREQUISITE DETECTED                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ Your query suggests: [detected pattern]                     │
│                                                              │
│ Architectural analysis works best after [prerequisite].     │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 1 - Run /[suggested_skill] "[suggested_prompt]"         │ │
│ │    [Brief explanation of what this does and why needed] │ │
│ │                                                          │ │
│ │ 2 - Continue with /arch anyway                          │ │
│ │    [Warning: may produce limited results without context]│ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
│ Response: "1" or "2"                                         │
└─────────────────────────────────────────────────────────────┘
```

**WAIT for user selection before proceeding.**

- If user selects "1": Execute `Skill(skill="<suggested_skill>", args="<suggested_prompt>")` and exit
- If user selects "2": Proceed to Stage 1 (IMPROVE_SYSTEM) or DEFAULT path

### No Prerequisite Detected

Proceed to **Stage 0.3: Codebase-Aware Analysis**.

---

## Stage 0.3: Codebase-Aware Analysis

**Read actual code before recommending changes to it.**

> See **Codebase-Aware Analysis (Stage 0.3)** in `shared_frameworks.md` for complete protocol.

If query references specific files, modules, or subsystems by name:
1. Glob/Grep to discover relevant files
2. Read top-level structure (first 50 lines, max 3 files for fast template)
3. Build internal CODEBASE CONTEXT block
4. Carry this context into all subsequent stages

Skip if query is purely theoretical or greenfield.

---

## Stage 0.6: Domain Resource Inclusion

**Before proceeding with decision path, check if domain-specific resources should be included.**

### Detect Default Domain

Check if a default domain is set:
- Environment variable: `ARCH_DEFAULT_DOMAIN`
- Conversation context: `conversation_context.get("default_domain")`

### Domain-Specific Resource Inclusion

If a domain is detected (default or keyword-based), include domain-specific considerations:

| Domain | Include When | Resource Sections |
|--------|--------------|-------------------|
| **python** | Default=python OR keywords detected | Async assessment, type hints, GIL considerations |
| **cli** | Default=cli OR keywords detected | POSIX compliance, signal handling, exit codes |
| **data-pipeline** | Default=data-pipeline OR keywords detected | ETL patterns, streaming vs batch, data quality |
| **precedent** | Default=precedent OR keywords detected | ADR format, decision documentation, precedent tracking |

### Python Domain Auto-Inclusion

**When python domain is active (default or detected), augment decision path with:**

1. **Async consideration** - Is this I/O-bound (asyncio) or CPU-bound (multiprocessing)?
2. **Type system** - What level of type precision is needed?
3. **Framework context** - FastAPI/Flask/Django implications
4. **GIL awareness** - Threading vs multiprocessing implications

**Do NOT switch to python.md template** - instead, inject Python-specific considerations into fast.md decision path.

### No Domain Detected

Proceed directly with generic fast.md decision path.

---

## Stage 0.7: Web Research

**Before proceeding with either IMPROVE_SYSTEM or DEFAULT path, conduct targeted web research.**

> See **Web Research Framework** section in `shared_frameworks.md` for complete protocol.
>
> **Reference:** `/.claude/skills/arch/resources/shared_frameworks.md` — "Web Research Framework" section

**For fast template: Use Targeted depth (1-2 searches, max 3).**

### Research Query Generation

From user's query, generate 1-2 focused searches:

1. **Current best practice** — What's the recommended approach for this specific pattern/problem right now?
2. **Version/deprecation check** — Are technologies involved current, or have breaking changes occurred?

### Execution

```
For each query (1-2 queries):
    1. WebSearch("[query]")
    2. WebFetch(top result) if needed for version/API details
    3. Extract: current recommendation, version info, key gotcha
```

### Integration

Weave findings into decision output — don't create a separate "research" section. Cite versions and sources inline.

### Skip Condition

Skip ONLY if: query is purely about user's internal system AND CKS has sufficient data, OR user explicitly requests offline analysis.

---

## IMPROVE_SYSTEM Path

### Your Definition of "Improve" Is Authoritative

No discovery phase. No clarifying questions.

**Your definition (final):**
- Improve = prevents repeated problems OR makes things faster
- System = named subsystem (memory, hooks, research, etc.)
- Source of truth = CKS.db memory entries (492 entries available)

### Stage 1: Query CKS for Failures (2–3 min)

**Check CKS availability using shared framework from `shared_frameworks.md`:**

> See **CKS Availability Check** section in `shared_frameworks.md` for complete implementation.
>
> **Reference:** `/.claude/skills/arch/resources/shared_frameworks.md` — "CKS Availability Check" section

**Summary:**
- Run CKS availability check code block from shared frameworks
- If CKS is NOT available, display `CKS_UNAVAILABLE_WARNING` from shared frameworks
- If CKS IS available, proceed with querying below

**If CKS IS available, query for memory entries using SEMANTIC SEARCH:**

```python
# Import semantic search function from routing module
from arch.routing import get_failure_history

# Extract subsystem from query
subsystem = "<extract from query: memory, hooks, CKS, research, retro, lesson, ingestion, validation, etc.>"

# Use semantic search to find failure history (Priority 1: Embedding Integration)
# This replaces keyword-based iteration with semantic similarity matching
failures = get_failure_history(subsystem=subsystem, limit=10)

# If no failures found, acknowledge and proceed
if not failures:
    print("Note: No CKS memory entries found for this subsystem.")
    print("Proceeding with generic best practices analysis.")
else:
    # Get top 2-3 unique failures (already deduplicated in get_failure_history)
    unique_failures = failures[:3]
```

**For each result, extract:**
1. What question was (the failure scenario)
2. What answer was (the fix or diagnosis)
3. Pattern type (detection, recovery, prevention, visibility gap)

**Format:**
```
FAILURE #1: [brief name from question]
- What happened: [extract from memory entry question]
- Fix/Solution: [extract from memory entry answer]
- Pattern: [detection/recovery/prevention/visibility gap]
```

### Stage 2: Extract Pattern (1 min)

From those 2–3 failures, identify:

**What class of problem repeats?**
- Detection gap (we didn't see it coming)?
- Recovery gap (saw it but took forever to fix)?
- Prevention gap (could have blocked it)?
- Visibility gap (failure is silent)?

One sentence max.

### Stage 3: Propose 1–2 Small Changes (2–3 min)

For EACH repeating pattern, propose ONE concrete change that:
1. Would have prevented or caught that failure, OR
2. Would have shortened diagnosis/fix time by >=50%

**Keep it small, testable, implementation-ready.**

**Required for each change:**

1. **What file(s) to create or edit**
   - Path (e.g., `/.claude/hooks/pre-delete-validator.ps1`)
   - New? Modify existing?

2. **Exact change (pseudocode or code)**
   - Hook logic, schema field, validation rule, script, etc.
   - Keep to 5–20 lines
   - Use `.ps1` or `.bat` for Windows (no `.sh`)

3. **How to test it**
   - One concrete scenario that triggers old failure
   - What new system should do differently
   - How to verify success

4. **Success metric**
   - "Caught before breaking research"
   - "Diagnosis < 5 min instead of 30 min"
   - "Automated suggestion instead of manual excavation"

**Example:**

```
Change A: Pre-delete module dependency check

File: /.claude/hooks/pre-delete-validator.ps1 (new)

Logic:
  # Runs before git rm on Python files
  $deletedFiles = git diff --staged --name-only | Select-String "\.py$"
  foreach ($file in $deletedFiles) {
    $moduleName = [System.IO.Path]::GetFileNameWithoutExtension($file)
    $pattern = "from lib import $moduleName|import .*\.$moduleName"
    $refs = Select-String -Path "P:/__csf/src/*","P:/.claude/*" -Pattern $pattern

    if ($refs) {
      Write-Host "⚠️  DEPENDENCY VIOLATION: $file still imported in:"
      $refs | ForEach-Object { Write-Host "  - $($_.Path)" }
      exit 1
    }
  }

Test:
  - Create dummy module with reverse import
  - Try `git rm` on it
  - Hook blocks deletion, shows import locations
  - Fix import, try again → succeeds

Success: Caught deletion before breaking tools
```

---

### Stage 4: Return Output

Format:

```
## Analysis: Improve [Subsystem Name]

### Failures Identified (from CKS)
[List 2–3 failures with what happened, fix/solution, pattern type]

### Pattern
[One sentence: class of repeating problem]

### Proposed Changes

**Change A:** [Name]
- File(s): [path]
- Logic: [pseudocode/exact lines]
- Test: [scenario]
- Success: [metric]

**Change B:** [Name] (optional)
- File(s): [path]
- Logic: [pseudocode/exact lines]
- Test: [scenario]
- Success: [metric]

### Implementation Order
1. Change [X] — easiest, highest payoff
2. Change [Y] — enables Change Z
3. Change [Z] — final hardening

Estimated effort: X hours total
```

---

## DEFAULT Decision Path

Your job: Answer "What's smallest change that solves this?"

**CONSTRAINTS:**
- Prefer local reordering, parameter changes, conditions
- Do NOT propose new services, modules, or layers
- Do NOT generate fake alternatives (2 real options max)
- Do NOT create lengthy timelines or tech debt estimates
- Keep output tight: 1–5 KB maximum

### Output Structure

#### 1. Decision Statement (1 paragraph)
What's changing, why, goal. Tight.

#### 2. Options (2–3 real ones)

> See **Forced Alternative Quality Gate** in `shared_frameworks.md`.

Each option must differ on at least one axis (technology, approach, coupling, etc.). Include a **Differs on:** line.

**Option A:** Proposed change
- Pro: [real benefit]
- Con: [real cost]
- **Differs on:** [axis]

**Option B:** Status quo or variant
- Pro: [real benefit]
- Con: [real cost]
- **Differs on:** [axis]

#### 3. Recommendation
One sentence: why A is better than B. Ground in research findings where available.

> See **Version Verification Rule** in `shared_frameworks.md` — verify any version/API claims.

#### 4. Implementation
Before/after code or pseudocode.
Rollback: how to undo.

#### 5. Quick Ramifications
- Break anything? (state if yes)
- Edge cases? (mention if subtle)
- Constraints? (quota, perf, UX?)

#### 6. Confidence

> See **Confidence Calibration Rules** in `shared_frameworks.md`.

One-line confidence with evidence basis:
```
Confidence: [X]% — [evidence summary]
```

#### 7. Adversarial Self-Review (Recommended)

> See **Adversarial Self-Review** in `shared_frameworks.md`.

One-line weakest assumption check:
```
Weakest assumption: [assumption]. If wrong: [consequence]. Mitigation: [action].
```

#### 8. Persist Output

> See **Output Persistence** in `shared_frameworks.md`.

Auto-save to `P:/.claude/arch_decisions/` unless output is under 2KB or user requests ephemeral.

```python
# Filename format (use actual datetime, do not hardcode date)
from datetime import datetime
date = datetime.now().strftime("%Y-%m-%d")
slug = re.sub(r'[^a-z0-9]+', '-', query[:50].lower()).strip('-')
filename = f"{date}_fast_{slug}.md"
```

---

## Resilience Considerations

**For I/O-bound operations:** Consider using `@with_resilience(profile='aggressive')` to handle transient errors
- Location: `P:/__csf/src/lib/resilience_patterns.py`
- Retry on: `ConnectionError`, `TimeoutError`, `TransientLLMError`
- No retry on: `InvalidUserInputError` (user errors should fail fast)

**For write operations:** Use `@with_resilience(profile='write_path', idempotent=False)`
- Minimal retries (max 1) to avoid duplicate side effects
- Circuit breaker prevents cascade failures

**Feature flags available:**
- `RESILIENCE_DISABLED_FOR=<skill_names>` — disable resilience for specific skills
- `RESILIENCE_OBSERVE_ONLY=true` — log without applying resilience patterns

**Import:**
```python
from src.lib.resilience_patterns import with_resilience, TransientLLMError, QuotaError
```

---

## Output Format

### Success Criteria

✅ IMPROVE_SYSTEM: Grounded in CKS memory entries
✅ IMPROVE_SYSTEM: Proposes small, testable changes
✅ IMPROVE_SYSTEM: No clarifying questions
✅ DEFAULT: Concise (1–5 KB)
✅ DEFAULT: No fake alternatives — quality gate enforced
✅ DEFAULT: Clear before/after
✅ DEFAULT: Confidence score with evidence basis
✅ Ready to implement now
