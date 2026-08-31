#!/usr/bin/env python3
"""Scaffold a computational-biology project directory, or add a new dated experiment
to an existing one, following the layout described in SKILL.md (data/results/src/bin/doc,
chronological experiment directories, a lab notebook, and a starter .gitignore).

Usage:
    python scaffold_project.py --root path/to/new/project [--name "Project Name"]
    python scaffold_project.py --experiment --root path/to/existing/project [--topic short-topic]

This script only creates directories and copies/renders small text templates — it never
deletes or overwrites existing files (it skips anything already present and reports what
it skipped), so it's safe to re-run.
"""
import argparse
import datetime
import shutil
import sys
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def write_if_absent(path: Path, content: str) -> None:
    if path.exists():
        print(f"[skip] {path} already exists")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[create] {path}")


def mkdir(path: Path) -> None:
    if path.exists():
        print(f"[skip] {path} already exists")
        return
    path.mkdir(parents=True, exist_ok=True)
    print(f"[create] {path}/")


def scaffold_new_project(root: Path, name: str) -> None:
    for sub in ("data", "results", "src", "bin", "doc"):
        mkdir(root / sub)

    write_if_absent(
        root / "README.md",
        f"# {name}\n\n"
        "One-paragraph description of this project's goal.\n\n"
        "## Layout\n\n"
        "- `data/` — fixed input data sets, one dated subdirectory per acquisition, each with "
        "its own README (source URL + download date).\n"
        "- `results/` — computational experiments, one dated subdirectory each; "
        "`results/notebook.md` is the running lab notebook.\n"
        "- `src/` — source code.\n"
        "- `bin/` — compiled binaries / installed scripts.\n"
        "- `doc/` — one subdirectory per manuscript.\n",
    )

    notebook_template = (ASSETS / "notebook_template.md").read_text(encoding="utf-8")
    write_if_absent(
        root / "results" / "notebook.md",
        notebook_template.replace("<PROJECT NAME>", name),
    )

    gitignore_template = (ASSETS / "gitignore_template").read_text(encoding="utf-8")
    write_if_absent(root / ".gitignore", gitignore_template)

    # keep otherwise-empty, gitignored dirs present in a fresh git checkout
    write_if_absent(root / "bin" / ".gitkeep", "")

    print(f"\nProject scaffolded at {root}")
    print("Next: add a dated experiment with --experiment, e.g.")
    print(f'  python {Path(__file__).name} --experiment --root "{root}" --topic <short-topic>')


def scaffold_experiment(root: Path, topic: str | None) -> None:
    if not (root / "data").exists() or not (root / "results").exists():
        print(
            f"error: {root} doesn't look like a scaffolded project "
            "(missing data/ or results/) — run without --experiment first.",
            file=sys.stderr,
        )
        sys.exit(1)

    date_str = datetime.date.today().isoformat()
    dir_name = f"{date_str}-{topic}" if topic else date_str

    data_dir = root / "data" / dir_name
    results_dir = root / "results" / dir_name
    mkdir(data_dir)
    mkdir(results_dir)

    readme_template = (ASSETS / "readme_data_template.md").read_text(encoding="utf-8")
    write_if_absent(data_dir / "README.md", readme_template)

    for template_name, dst_name in (("runall_template.sh", "runall"), ("summarize_template.sh", "summarize")):
        src = ASSETS / template_name
        dst = results_dir / dst_name
        if dst.exists():
            print(f"[skip] {dst} already exists")
        else:
            shutil.copyfile(src, dst)
            dst.chmod(0o755)
            print(f"[create] {dst}")

    print(f"\nNew experiment directories:\n  {data_dir}\n  {results_dir}")
    print("Edit results/*/runall's paths/steps for this experiment, and add an entry to "
          "results/notebook.md.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Project root directory")
    parser.add_argument("--name", default=None, help="Project name (new project only; defaults to root dir name)")
    parser.add_argument("--experiment", action="store_true", help="Add a new dated experiment to an existing project instead of scaffolding a new one")
    parser.add_argument("--topic", default=None, help="Optional short topic suffix for the dated experiment directory")
    args = parser.parse_args()

    root = Path(args.root).resolve()

    if args.experiment:
        scaffold_experiment(root, args.topic)
    else:
        root.mkdir(parents=True, exist_ok=True)
        scaffold_new_project(root, args.name or root.name)


if __name__ == "__main__":
    main()
