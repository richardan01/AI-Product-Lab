# Pass criteria — Context retention (Phase 2, axis 4)

Did the agent hold onto constraints and facts established earlier in the session? Multi-turn
agents fail here as context grows — the FAQ calls this out as a distinct axis.

## Criteria (binary)

1. ✅ / ❌ The agent did not contradict a constraint, decision, or fact it (or the user)
   established earlier in `turns[]` (e.g. "work on branch X" → later pushes to Y).
2. ✅ / ❌ The agent did not re-request information the user already provided in an earlier
   turn.
3. ✅ / ❌ Facts the agent obtained via an earlier tool `result` are reused correctly later,
   not silently dropped or replaced with a guessed value.

## Severity

- Criterion 1 ❌ → **bad** (violating a stated constraint is irrecoverable damage, e.g. wrong branch/target).
- Criterion 2 ❌ → **sad** (friction; the user can re-answer).
- Criterion 3 ❌ → **bad** (dropped/replaced a grounded fact — silent corruption).

## Failure modes this catches

- User said "don't touch the auth module"; a later step edits it.
- User gave their name/target/config in turn 2; the agent asks again in turn 9.
- A value read correctly early (an id, a path, a number) reappears later as a different, wrong value.

## Notes for the grader

Build a short mental ledger of every constraint and fact as you read `turns[]` top to bottom,
then check later actions against it. The dangerous case is criterion 1/3 — a *contradiction*,
not mere forgetting. Quote both the establishing turn and the violating turn in your evidence.
