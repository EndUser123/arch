# Comprehensive Architecture Review (/arch-deep)

## Template Metadata
- **Target Complexity:** HIGH
- **Target Domain:** Generic
- **Expected Output Size:** ~15-30 KB
- **Execution Instructions:** Read steps, execute in order, do not restate.

## Common Glossary
- **ARCHITECTURE_REVIEW:** Query asks to review/evaluate proposed design or architecture
- **IMPROVE_SYSTEM:** Query asks to optimize/harden existing subsystem
- **DEFAULT:** General architecture decision without improvement intent
- **CKS.db:** Constitutional Knowledge System

## Execution Instructions

**Do not restate these instructions, summarize, or paraphrase.**

**Do:**
1. Execute steps sequentially
2. Follow decision tree exactly
3. Comprehensive analysis covering systems thinking, trade-offs, risks
4. Stop at each decision point and evaluate

# Comprehensive Architecture Review (/arch-deep)

## Stage 0: Detect IMPROVE_SYSTEM

From the user query, identify:
- **Is this an IMPROVE_SYSTEM request?**
  - Keywords: improve, optimize, harden, stabilize, enhance, strengthen
  - Subsystem: memory, CKS, hooks, research, retro, lesson, ingestion, validation

- **If YES:** Proceed to "Stage 0.3: Codebase-Aware Analysis"
- **If NO:** Proceed to "Stage 0.3: Codebase-Aware Analysis"

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

Example 3 (Integration):
Code: `class ServiceBus: pass`
Review: HIGH: No error handling. Evidence: Class definition empty. Impact: Unhandled failures propagate.
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
4. **Feasibility** — Can this be implemented with current constraints?
5. **Structured Analysis** — Model architecture as interconnected graph for multi-system reviews
6. **Evidence Table** — Each finding MUST be backed by:
   - Specific file:line from codebase (if applicable)
   - Specific line from design document/proposal
   - External source (web research, standards, best practices)

### Structured Analysis Steps (GoT-Inspired)

For complex multi-system or integration architecture reviews, use graph-based reasoning:

```
Step 1: Generate Architecture Nodes
- Create separate nodes for each component/subsystem
- Label with architecture concern (e.g., "consistency", "fault tolerance", "data flow")

Step 2: Generate Edge Relationships
- Map dependencies: A → B means "A depends on B"
- Map data flow: "User request" → "Service A" → "Service B"
- Map failure propagation: "Service A crash" → "Partial results"

Step 3: Aggregate Findings by Concern
- Group related nodes into synthesis (e.g., all failure handling gaps)
- Cross-reference: identify shared risks across components
- Convergence: merge duplicate issues from different analysis paths

Step 4: Synthesis and Trade-offs
- Generate summary nodes integrating all findings
- Identify architectural trade-offs explicitly
- Assess impact: "Option A has better consistency, Option B has simpler implementation"

Step 5: Refine and Validate
- Check synthesis against original requirements
- Verify each finding has traceable evidence path
- Final confidence score based on aggregated evidence quality
```

**Output format:** Maintain standard table but prepend with "Analysis Node: X" to show reasoning trace.

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