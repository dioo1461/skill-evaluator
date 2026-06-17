# Patch Mode

Load this only when the user asks to improve, patch, or apply fixes to the evaluated skill.

1. Complete a concise evaluation first, including validation status and prioritized P0/P1/P2 findings.
2. Preserve the evaluated skill's intended purpose unless the user changes it or explicitly approves a direction-level change.
3. Separate implementation-level fixes from direction-level changes. Direction-level changes include changing the target user, primary use case, trigger scope, output artifact type, success criteria, or core workflow ownership.
4. Do not apply direction-level changes without explicit user approval; report them as approval-gated recommendations unless the user has already requested that direction change.
5. Fix P0/P1 items first, then P2 items if they are scoped and low risk.
6. Keep `SKILL.md` concise. Move optional detail into directly referenced resources only when it reduces always-loaded context or update burden.
7. Update `agents/openai.yaml` when display metadata becomes stale.
8. Do not create extra documentation files such as README, changelog, or implementation notes unless the user explicitly asks.
9. Re-run the same safe validators or manual structural checks after editing.
10. Re-run the evaluation rubric against the changed files and report the before/after score.

If editing is partially blocked, report which priority items remain unresolved and how they affect the score.
