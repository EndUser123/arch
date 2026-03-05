# CLI Architecture Analysis

## Template Metadata
- **Target Complexity:** Any
- **Target Domain:** CLI/POSIX
- **Expected Output Size:** ~8 KB
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
3. CLI/POSIX specific analysis
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

If query references specific CLI code/modules, read them first. Build CODEBASE CONTEXT.

---

## Stage 0.7: Web Research

**Conduct targeted web research before analysis.**

> See **Web Research Framework** in `shared_frameworks.md` for complete protocol.

**For cli template: Use Domain-focused depth (2-3 searches, max 5).**

Focus searches on:
1. **CLI framework status** — Current versions of Click/Typer/argparse, new features, deprecations
2. **POSIX compliance updates** — Shell compatibility gotchas, cross-platform CLI patterns
3. **CLI UX best practices** — Current thinking on progress indicators, error messages, color output

Integrate findings inline. Cite version numbers and sources.

---

## IMPROVE_SYSTEM

**Goal:** Optimize or harden existing CLI code.

### Step 1: Current State Analysis

1. **Identify CLI framework in use:**
   - Click? Typer? argparse? Cliff? Other?
   - Check `requirements.txt`, `pyproject.toml`, or imports

2. **Analyze POSIX compliance:**
   - Exit codes: Does it use 0 for success, non-zero for errors?
   - stdout/stderr: Are they correctly separated?
   - Signal handling: Does it handle SIGINT/SIGTERM gracefully?

3. **Check terminal awareness:**
   - Terminal size detection?
   - Progress bars?
   - Color output with NO_COLOR respect?
   - Pagination for long output?

### Step 2: Identify Improvement Areas

Based on findings from Step 1:

- **Exit codes:** Are they well-defined and POSIX-compliant?
- **Error handling:** Are user errors distinguished from system failures?
- **Help text:** Is it clear, complete, and auto-generated?
- **Shell integration:** Completions? Config files? Environment variables?
- **Signal handling:** Graceful shutdown on Ctrl+C?

### Step 3: Recommend Specific Improvements

For each area needing improvement:

1. **What's missing?** (gap analysis)
2. **Why it matters** (POSIX/UX rationale)
3. **How to fix** (code pattern or library recommendation)
4. **Risk level** (breaking change vs additive)

---

## DEFAULT

**Goal:** Make general CLI architecture decisions.

### CLI Concerns

#### POSIX Standards
- **Exit codes:** 0 = success, 1 = error, 2+ = application-specific
- **stdout vs stderr:** Regular output to stdout, errors/diags to stderr
- **Signals:** Handle SIGINT (Ctrl+C), SIGTERM gracefully
- **Pipelines:** Design for composable single-purpose tools

#### Argument Parsing
- **Click:** Best DX, decorators, automatic help, shell completion
- **Typer:** Click-based, modern type hints, less boilerplate
- **argparse:** Stdlib only, verbose, but no external deps
- **Cliff:** Multi-command apps like git, nested subcommands

#### Terminal Awareness
- **Terminal size:** Detect with `shutil.get_terminal_size()`
- **Progress bars:** `click.progressbar` or `tqdm`
- **Colors:** ANSI codes, but respect `NO_COLOR` env var
- **Pager:** Paginate long output (`less` integration)

---

## Stages

All standard /arch-deep stages, PLUS:

### CLI Stage 1: Command Structure
- Single-purpose tool vs multi-command app?
- Subcommands needed?
- Flag conventions (GNU style `--long`, `-short`)

### CLI Stage 2: Exit Code Strategy
- Define all exit codes
- Distinguish user errors vs system failures
- Signal handling for graceful shutdown

### CLI Stage 3: Shell Integration
- Completion scripts needed?
- Config file locations (XDG base dir)?
- Environment variable conventions?

---

## Patterns

### Command Template
```python
import click
import sys

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', help='Output file')
def main(input_file, output):
    """Single-purpose tool with clear exit codes."""
    try:
        process(input_file, output)
        sys.exit(0)
    except click.ClickException as e:
        e.show()
        sys.exit(e.exit_code)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)
```

### Multi-Command App
```python
@click.group()
def cli():
    """My CLI app with subcommands."""
    pass

@cli.command()
def init():
    """Initialize project."""
    pass

@cli.command()
def build():
    """Build project."""
    pass
```

### Graceful Shutdown
```python
import signal

class ShuttingDown:
    def __init__(self):
        self.shutdown = False

    def signal_handler(self, signum, frame):
        self.shutdown = True
        click.echo("\nShutting down gracefully...", err=True)
```

---

## Output Format

Structure your recommendation as:

### 1. Framework Recommendation
- **Chosen framework:** [Click/Typer/argparse/Cliff/Other]
- **Rationale:** Why this fits use case
- **Trade-offs:** What you're giving up

### 2. Architecture Pattern
- **Single-command vs multi-command:**
- **Subcommands needed:** List if applicable
- **Flag style:** GNU style (`--long`, `-short`)

### 3. POSIX Compliance Checklist
- [ ] Exit codes defined
- [ ] stdout/stderr separated
- [ ] Signal handling implemented
- [ ] Pipeline-friendly output

### 4. Terminal UX
- [ ] Help text completeness
- [ ] Progress indicators (if applicable)
- [ ] Color output with NO_COLOR respect
- [ ] Pagination (if applicable)

### 5. Shell Integration
- [ ] Completion scripts (bash/zsh/fish)
- [ ] Config file locations (XDG)
- [ ] Environment variable conventions

---

## Success Criteria

- POSIX-compliant exit codes
- stdout/stderr correctly separated
- SIGINT/SIGTERM handled gracefully
- Help text clear and complete
- Colors respect NO_COLOR
- Terminal size awareness (if applicable)
- Config follows XDG conventions

---

## Final Output Block

**Decision:** [One sentence recommendation]

**Rationale:** [2-3 key reasons, domain-specific]

**Alternatives Considered:** [Brief list with domain trade-offs]
> Apply **Forced Alternative Quality Gate** — each alternative must differ on at least one axis.

**Risk:** [Domain-specific risks]

> Apply **Version Verification Rule** — verify all CLI framework version/API claims against official docs.

**Confidence:** [X]% — [evidence basis]
> Apply **Confidence Calibration Rules** from `shared_frameworks.md`.

**Adversarial Self-Review:** (Recommended)
> One-line weakest assumption + consequence per `shared_frameworks.md`.

**Persist:** Auto-save to `P:/.claude/arch_decisions/` per **Output Persistence** protocol.

```python
# Filename format (use actual datetime, do not hardcode date)
from datetime import datetime
date = datetime.now().strftime("%Y-%m-%d")
slug = re.sub(r'[^a-z0-9]+', '-', query[:50].lower()).strip('-')
filename = f"{date}_cli_{slug}.md"
```

---

## Resilience Considerations

**For CLI tools calling external APIs:** Consider using `@with_resilience(profile='conservative')`
- Location: `P:/__csf/src/lib/resilience_patterns.py`
- Retry on: `ConnectionError`, `TimeoutError`, `QuotaError`
- No retry on: `InvalidUserInputError` (user errors should fail fast with clear error messages)

**For read operations (config, cache reads):** Use `@with_resilience(profile='read_only', idempotent=True)`
- More retries (max 3) for idempotent reads
- Safe to retry on file system reads

**For write operations:** Use `@with_resilience(profile='write_path', idempotent=False)`
- Minimal retries (max 1) to avoid duplicate side effects
- Respect POSIX exit code conventions even after retries

**Feature flags:**
- `RESILIENCE_DISABLED_FOR=<skill_names>` — disable resilience for specific CLI commands
- `RESILIENCE_OBSERVE_ONLY=true` — log without applying resilience patterns

**Import:**
```python
from src.lib.resilience_patterns import with_resilience, TransientLLMError, QuotaError
```

---
*End of CLI template. Falls back to generic decision format.*
