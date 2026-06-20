# Patch Mode

Load this only when the user asks to improve, patch, or apply fixes to the evaluated skill.

1. Complete a concise evaluation first, including validation status and prioritized P0/P1/P2 findings.
2. Before the first edit to a local skill artifact, create a timestamped backup outside the evaluated skill directory, preferably under `$CODEX_HOME/skill-backups/<skill-name>/<timestamp>/` or `~/.codex/skill-backups/<skill-name>/<timestamp>/` when `$CODEX_HOME` is unavailable. Preserve relative paths for files being edited; for broad or uncertain edits, back up the whole skill directory. If an active Codex goal identifier or short objective label is available, include it in the backup folder name when practical, but do not create a goal solely for backup naming.
3. Do not edit until the backup succeeds, unless the target is pasted content, a remote-only artifact, a diff without local source files, or the user explicitly approves proceeding without a backup. Report the backup path, skipped backup reason, or backup failure in the final patch summary.
4. Preserve the evaluated skill's intended purpose unless the user changes it or explicitly approves a direction-level change.
5. Separate implementation-level fixes from direction-level changes. Direction-level changes include changing the target user, primary use case, trigger scope, output artifact type, success criteria, or core workflow ownership.
6. Do not apply direction-level changes without explicit user approval; report them as approval-gated recommendations unless the user has already requested that direction change.
7. Fix P0/P1 items first, then P2 items if they are scoped and low risk.
8. Keep `SKILL.md` concise. Move optional detail into directly referenced resources only when it reduces always-loaded context or update burden.
9. Update `agents/openai.yaml` when display metadata becomes stale.
10. Do not create extra documentation files such as README, changelog, or implementation notes unless the user explicitly asks.
11. Re-run the same safe validators or manual structural checks after editing.
12. Re-run the evaluation rubric against the changed files and report the before/after score.

If editing is partially blocked, report which priority items remain unresolved and how they affect the score.
