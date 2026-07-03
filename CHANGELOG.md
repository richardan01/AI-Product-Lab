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
