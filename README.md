# Taskforge

Taskforge is a small command-line task tracker built with the Python standard library.
It stores tasks in a JSON file and supports adding, listing, completing, searching, and reporting.

## Run

```bash
python -m taskforge add "Write lab report" --priority high --tag school
python -m taskforge list --status open
python -m taskforge complete 1
python -m taskforge report
```

The default data file is `.taskforge.json` in the current directory. Use `--data PATH`
to select another file.

## Test

```bash
python -m unittest discover -s tests -v
```

The codebase intentionally includes TODO and FIXME comments as maintenance markers for
future exercises and code-reading practice.
