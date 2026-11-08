# slim-claude-md

A Claude Code skill that shrinks a bloated `CLAUDE.md`.

`CLAUDE.md` is read in full at the start of every session. Over a long project
it fills up with dated status notes and decisions, and every one of them costs
tokens in every session. This skill moves that history, **word for word**, into
topic files under `docs/notes/`, leaves a short `CLAUDE.md` with the rules you
need every time plus an index, and checks line by line that nothing was lost.

Real example: a 202 KB `CLAUDE.md` (about 50,000 tokens per session) became
14 KB, with every line kept in seven notes files.

## Install

```bash
git clone https://github.com/hustle-x/slim-claude-md.git
cp -r slim-claude-md/slim-claude-md ~/.claude/skills/
```

Or paste this into Claude Code:

```
Install the skill from https://github.com/hustle-x/slim-claude-md
```

## Use

In a project, say *"slim my CLAUDE.md"* (or run `/slim-claude-md`).

It will back up the file, sort lines into keep and move, write
`docs/notes/<topic>.md`, write the short `CLAUDE.md` with an index, and run
`verify.py`, which fails if any line went missing.

`verify.py` is standard-library Python 3 and never touches the network:

```bash
python3 slim-claude-md/verify.py CLAUDE.before.md CLAUDE.md docs/notes/*.md
```

## License

MIT
