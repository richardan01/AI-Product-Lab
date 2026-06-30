# Workflow: Feature Kickoff (Multi-Agent Handoff)

**Purpose:** This workflow chains four agents together to process raw meeting notes into a full product pipeline. It demonstrates how Claude Code can act as the "Orchestrator" running a sequential pipeline.

**Trigger:** You just finished a messy brainstorming session with stakeholders about a new use case. You dumped the raw, unformatted notes into `_temp/raw-meeting-notes.md`.

---

## Instructions for Claude Code

When the user runs this workflow, execute the following steps in exact order. **Do not stop until all 4 steps are complete.**

### Step 1: Stakeholder Manager (Clean & Structure)
* **Action:** Read `_temp/raw-meeting-notes.md`.
* **Prompt:** "Act as the Stakeholder Manager. Clean up these raw notes following the `Templates/1on1-notes.md` structure. Identify the core decisions made in the session. Save the output to `Meetings/one-offs/[meeting-name].md`."

### Step 2: Product Definer (Extract Requirements)
* **Action:** Read the newly created meeting notes file.
* **Prompt:** "Act as the Product Definer. Extract all product requirements from these notes. Draft a structured PRD using `Templates/prd.md`. Focus heavily on the acceptance criteria for the key technical components. Save the output to `Projects/[project]/prd-[use-case-name].md`."

### Step 3: Task Manager (Ticket Creation)
* **Action:** Read the new PRD.
* **Prompt:** "Act as the Task Manager. Parse the PRD and extract actionable engineering and PM tasks. Format them as checklist items with `#p0` or `#p1` tags. Append these tasks to the bottom of `Tasks/backlog.md`."

### Step 4: Domain Specialist (Project Status Update)
* **Action:** Read the original meeting notes and the new PRD.
* **Prompt:** "Act as the Domain Specialist. Update the `Projects/[project]/brief.md` file. Specifically, update the 'Open Questions' section if any were answered in the meeting, and update the 'Use Case Candidates' to reflect the decisions made."

---

## Completion Criteria
When finished, the Orchestrator (Claude) should output a single summary to the user:
- Link to the structured meeting notes.
- Link to the draft PRD.
- Confirmation that tasks were added to the backlog.
- Confirmation that the project brief was updated.
