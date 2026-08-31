# compbio-project-organizer

A [Claude Code](https://claude.com/claude-code) skill that gives Claude practical guidance and
tooling for structuring computational biology / bioinformatics projects on disk: directory
layout, lab notebooks, driver scripts, error handling, and version control.

The guidance is distilled from:

> Noble WS (2009) A Quick Guide to Organizing Computational Biology Projects. PLOS Computational Biology 5(7): e1000424. https://doi.org/10.1371/journal.pcbi.1000424

This repository is not affiliated with the author; it's a practical restatement of the paper's principles as a Claude Code skill, plus a scaffolding script (`scripts/scaffold_project.py`) that generates the recommended directory skeleton.

## What's here

- `SKILL.md` — the skill definition Claude Code loads: the two guiding principles, directory layout, lab notebook format, driver script rules, error handling, and a review checklist for auditing an existing project.
- `scripts/scaffold_project.py` — generates a new project skeleton (`data/ results/ src/ bin/ doc/`), or adds a new dated experiment directory to an existing project.
- `assets/` — templates used by the skill and scaffold script: a lab notebook entry format, `runall`/`summarize` driver-script skeletons, a data-directory README template, and a starter `.gitignore`.

## Installing

Clone into a skills directory Claude Code reads from — either globally:

```bash
git clone https://github.com/dmkv1/compbio-project-organizer.git ~/.claude/skills/compbio-project-organizer
```

or into a single project:

```bash
git clone https://github.com/dmkv1/compbio-project-organizer.git .claude/skills/compbio-project-organizer
```

Claude Code will pick it up automatically and invoke it when a conversation touches computational-biology project organization.

## License

The original material here — `SKILL.md`'s wording, the scaffold script, and the templates — is
MIT licensed (see [LICENSE](LICENSE)). The directory layout, rules, and principles they describe
are drawn from Noble WS (2009), licensed CC BY 4.0 by PLOS; the MIT grant covers this repo's
expression of that guidance, not the underlying methodology or the paper itself.

