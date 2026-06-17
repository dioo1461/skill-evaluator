---
name: release-note-auditor
description: Audit release-note drafts against shipped changes, risk labels, and customer-facing language. Use for release-note quality checks and changelog readiness. Do not use for writing marketing copy, editing unrelated docs, or reviewing source code style.
---

# Release Note Auditor

## Purpose

Use this skill to verify that release notes accurately describe shipped behavior, call out user-visible risks, and avoid internal implementation detail.

## Inputs

- Release-note draft or changelog section.
- Diff, merged PR list, issue list, or deployment summary.
- Product or support guidance when available.

Ask one concise question only if no release-note text or shipped-change source is available.

## Workflow

1. Resolve scope.
   - Identify the release version, date, changed artifacts, and audience.
   - Mark missing sources as unknown instead of inventing shipped behavior.

2. Inspect evidence progressively.
   - Read the release-note draft first.
   - Inspect only the PRs, issues, diffs, or deployment records needed to verify each claim.
   - Record uninspected sources when the release bundle is too large to inspect fully.

3. Check accuracy and risk.
   - Match each user-facing claim to shipped evidence.
   - Flag omitted breaking changes, migration notes, known limitations, or support-impacting risks.
   - Separate factual errors from tone or completeness suggestions.

4. Validate output.
   - Confirm every recommended edit has a source reference.
   - If sources disagree, report the conflict and avoid rewriting the note as fact.
   - Do not approve the release note when any user-visible change lacks enough evidence.

5. Report.
   - Lead with blockers, then factual corrections, then optional wording polish.
   - Include a concise approval status: `ready`, `ready with edits`, or `blocked`.

## Safety

Do not publish release notes, modify issue trackers, or contact customers. Redact unreleased customer names, credentials, and incident details unless they are already approved for the release note.
