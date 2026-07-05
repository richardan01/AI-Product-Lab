# Changelog

All notable changes to this project will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). This project anchors entries to lab capability milestones, not package releases.

---

## [Unreleased]

### Added
- `AGENTIC-EVAL-FRAMEWORK.md` — the eval-loop framework manifesto: problem, loop design, architecture layers, metrics, and portfolio framing (consolidated from PM Command Center)
- `GEMINI.md` — harness-neutral entry point for Gemini CLI; the lab now routes Claude Code and Gemini CLI to the same configuration surface
- Sub-agent library in `.claude/agents/` — bounded worker contexts (drafting, research, parsing, context extraction) that skills compose instead of doing everything monolithically (consolidated from PM Command Center)
- Skills: `/eod` (end-of-day loop closure), `/competitive-analysis`, `/user-personas`, `/opportunity-solution-tree`, `/pre-mortem` (consolidated from PM Command Center)
- `.markdownlint.json` + `.markdownlintignore` — lint ruleset for template-compatible markdown; eval run evidence excluded (verbatim capture)
- CI: markdownlint + placeholder-residue steps added to the quality-gates workflow

### Changed
- PM Command Center (`richardan01/PM-Command-Center`) consolidated into this repo and retired; AI Product Lab is now the single public PM-OS surface
- Gate docs (`CLAUDE.md`, `HOW-IT-WORKS.md`, `Workflows/gate-merge.md`, reviewer skills) rewritten to describe the real hook behavior: all four write tools + Bash write-commands are gated, markers are per-artifact bound, and the hook fails closed
- `Evals/index.md` is now the canonical suite registry (adds build-review / go-nogo / research-sufficiency / monitoring); `Evals/evals-hub.md` points at it instead of listing a divergent set

### Fixed
- **Adversarial review of the OS** (`/codex:adversarial-review`, 2026-07-05) — three parallel audits (structure, gate enforcement, skills/evals/memory). Reference/consistency fixes:
  - Three wrong thesis paths (`alfred`, `nightwing`, `henri-ducard` pointed at a non-existent `Bruce-Wayne/` directory) and Nightwing's non-existent write dirs → corrected to real paths
  - Vicki Vale model id `claude-sonnet-5` → `claude-sonnet-4-6` (matches the tier table)
  - All 8 agent frontmatters normalized to `Batman Strategic Layer`
  - Removed references to unshipped skills (`/technical-depth-builder`, `/model-eval-design`, `/public-artifact-publishing`) and broken `batman/` wikilinks
  - Corrected the "ships only the eval trio" claim in `agent-system-architecture.md` (all 14 workers ship); reworded the Gordon and `MEMORY.md` lines to reflect what actually ships
  - Removed 5 phantom `Templates/*` rows from `Evals/_ci-map.md`; pointed `concepts-index` at the shipped `pm-decisions-log.template.md`

### Security
- **Publish-gate hardening** (`Tools/gate-check.sh`, `.claude/settings.json`, `.gitignore`) — closed the bypasses the adversarial review found:
  - Bash writes into gated paths (`cat > Artifacts/x.md`, `tee`, `cp`, `mv`, `sed -i`, `touch`) now blocked — the PreToolUse matcher previously excluded `Bash` entirely
  - Markers are validated by content, not just mtime: a `touch`ed/empty marker no longer arms the gate; each marker is bound to the artifact filename it reviewed (`File:` basename + `Verdict: PASS|CONDITIONAL`), so one review can no longer ship a different unreviewed artifact
  - Bash commands that create/modify the `_Registry` markers are blocked (the `rm` disarm stays allowed)
  - Hook fails **closed** on malformed input, missing `file_path`, or any internal error; case-insensitive `Artifacts/` match; symlink-aware; `GATE_TTL_SECONDS` clamped to the 6h ceiling; no-`python3` shell fallback hardened to match
  - Live `_Registry/.riddler-passed` / `.vicki-passed` / `.vicki-bounced` markers gitignored so a committed marker can't get a fresh mtime on checkout and permanently arm the gate
  - Verified with a 15-case gate-check test matrix plus shell-fallback, fail-closed, and TTL-clamp cases

## [1.1.0] — 2026-07-02

### Added
- Eval parity stack; artifact gate hook (`Tools/gate-check.sh`) with TTL + filename-pattern gating
- `scripts/` CI runners: repo hygiene, artifact-gate verification, eval-freshness sentinel

### Changed
- Renamed public positioning from AIPM-OS to **AI Product Lab**
- Made the repo a standalone demo: stripped day-job layer

### Fixed
- `gate-check.sh` path-canonicalization bypass

## [1.0.0] — 2026-06-30 / 2026-07-01

### Added
- Initial public release: AI PM OS + RegEval harness (LLM-as-judge, Cohen's κ, held-out generalization)
- Proof-of-work repo overview (`PROOF-OF-WORK.md`)

### Changed
- Genericized for public release: removed identity leaks, fixed 8-agent inconsistency, aligned portfolio-lab positioning
