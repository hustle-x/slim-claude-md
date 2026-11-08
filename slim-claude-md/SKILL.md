---
name: slim-claude-md
description: Shrinks a bloated CLAUDE.md that is loaded into every session by moving its history and status notes, word for word, into topic files under docs/notes/ and leaving a short CLAUDE.md with the always-needed rules plus an index. Verifies line by line that nothing was lost and keeps a backup. Use when the user says "CLAUDE.md is too big", "slim / trim / split CLAUDE.md", "save tokens on CLAUDE.md", or when a CLAUDE.md is over ~25 KB.
---

# Slim CLAUDE.md

A CLAUDE.md is read in full at the start of every session. Logs of past work
pile up in it and cost tokens every time, though they are needed only when
working on that topic. This skill moves them out without losing a word.

Rules: never delete, summarise or reword moved text; never touch code or other
config; never change the meaning of what stays. The only edits allowed in kept
lines are facts the user just changed in this session.

## Steps

1. **Measure.** `wc -c CLAUDE.md`. About 4 bytes = 1 token. Under ~25 KB:
   say it is already small and stop unless the user still wants it.
2. **Back up.** Copy CLAUDE.md somewhere outside the repo (the scratchpad, or
   `CLAUDE.before.md` if the user wants it kept) before writing anything.
3. **Map it.** List every line with its number, length and first ~90
   characters (`awk '{printf "%d [%d] %s\n", NR, length($0), substr($0,1,95)}' CLAUDE.md`).
   Sort lines into:
   - **Keep** (needed in almost every session): what the project is, current
     status in 2-3 lines, how to build / run / test / install / release /
     deploy, secrets and account rules, rules for working with the user,
     tool rules (e.g. graphify), design rules that still apply.
   - **Move**, grouped by topic (a feature, a product, a subsystem, a phase):
     dated status logs, changelogs, decisions already built in, previews,
     rejected ideas, old versions.
   When unsure, keep it. Show the user the plan (files and what goes where)
   if they asked to review first; otherwise go ahead.
4. **Write the notes.** One file per topic in `docs/notes/<topic>.md`, each
   starting with a `# Title` and the line `Moved word for word from CLAUDE.md
   on <date>.`, then the moved lines copied by line number (use a script, not
   retyping: retyping loses words).
5. **Write the short CLAUDE.md**: the kept lines in their original order, a
   `## Status` line with today's state, and a `## Notes` index: one bullet per
   notes file naming what is in it, plus the rule *"read the matching file
   before working on that topic; add new status notes to the end of the
   matching notes file, not here."*
6. **Verify.** Run
   `python3 <this skill's folder>/verify.py BACKUP CLAUDE.md docs/notes/*.md`.
   It must print `OK`. If it lists missing lines, put them back and run it
   again.
7. **Report** in one short message: old and new size, tokens saved per
   session, the notes files, where the backup is, and that nothing was
   removed.

## Afterwards

When adding a new note later in the project, append it to the matching
`docs/notes/` file (or a new topic file listed in the index), never to the
short CLAUDE.md.
